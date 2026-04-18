---
name: aws-iac-patterns
description: "Padrões de IaC AWS com Terraform: módulos, remote state, IAM, networking e ambiente multi-env. Use quando configurar infra AWS, criar módulos Terraform, ou revisar IaC AWS."
---

# AWS Infrastructure as Code — Terraform Patterns

Padrões de infraestrutura AWS com Terraform.

## Estrutura multi-ambiente

```
iac/terraform/
├── modules/
│   ├── lambda/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── sqs/
│   ├── dynamodb/
│   ├── api-gateway/
│   └── networking/
├── environments/
│   ├── dev/
│   │   ├── main.tf           # Usa os módulos
│   │   ├── variables.tf
│   │   ├── terraform.tfvars
│   │   └── backend.tf        # S3 state para dev
│   ├── staging/
│   └── prod/
└── global/
    ├── iam/                   # IAM roles compartilhados
    └── state-backend/         # S3 bucket + DynamoDB para state
```

## Remote state setup
```hcl
# global/state-backend/main.tf
resource "aws_s3_bucket" "terraform_state" {
  bucket = "mycompany-terraform-state"

  lifecycle { prevent_destroy = true }
}

resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration { status = "Enabled" }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"
    }
  }
}

resource "aws_dynamodb_table" "terraform_lock" {
  name         = "terraform-lock"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  attribute {
    name = "LockID"
    type = "S"
  }
}
```

```hcl
# environments/dev/backend.tf
terraform {
  backend "s3" {
    bucket         = "mycompany-terraform-state"
    key            = "dev/terraform.tfstate"
    region         = "sa-east-1"
    dynamodb_table = "terraform-lock"
    encrypt        = true
  }
}
```

## Módulo Lambda reutilizável
```hcl
# modules/lambda/variables.tf
variable "function_name" { type = string }
variable "handler" { type = string }
variable "runtime" { type = string }
variable "memory_size" { type = number; default = 256 }
variable "timeout" { type = number; default = 30 }
variable "environment_variables" { type = map(string); default = {} }
variable "policy_arns" { type = list(string); default = [] }
variable "environment" { type = string }
variable "service" { type = string }

# modules/lambda/main.tf
locals {
  full_name = "${var.service}-${var.function_name}-${var.environment}"
  common_tags = {
    Environment = var.environment
    Service     = var.service
    ManagedBy   = "terraform"
  }
}

resource "aws_lambda_function" "this" {
  function_name = local.full_name
  handler       = var.handler
  runtime       = var.runtime
  memory_size   = var.memory_size
  timeout       = var.timeout
  role          = aws_iam_role.lambda.arn

  environment {
    variables = var.environment_variables
  }

  tags = local.common_tags
}

resource "aws_lambda_alias" "live" {
  name             = var.environment
  function_name    = aws_lambda_function.this.function_name
  function_version = aws_lambda_function.this.version
}

resource "aws_iam_role" "lambda" {
  name = "${local.full_name}-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
  tags = local.common_tags
}

resource "aws_iam_role_policy_attachment" "basic" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy_attachment" "custom" {
  for_each   = toset(var.policy_arns)
  role       = aws_iam_role.lambda.name
  policy_arn = each.value
}

# modules/lambda/outputs.tf
output "function_name" { value = aws_lambda_function.this.function_name }
output "function_arn" { value = aws_lambda_function.this.arn }
output "alias_arn" { value = aws_lambda_alias.live.arn }
output "role_arn" { value = aws_iam_role.lambda.arn }
```

## IAM — Menor privilégio

### Padrão: policy por recurso
```hcl
# DynamoDB — apenas as ações necessárias na tabela específica
resource "aws_iam_policy" "dynamodb_orders" {
  name = "${local.full_name}-dynamodb-orders"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:UpdateItem",
        "dynamodb:Query",
      ]
      Resource = [
        aws_dynamodb_table.orders.arn,
        "${aws_dynamodb_table.orders.arn}/index/*",
      ]
    }]
  })
}

# SQS — apenas receive e delete na fila específica
resource "aws_iam_policy" "sqs_consume" {
  name = "${local.full_name}-sqs-consume"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "sqs:ReceiveMessage",
        "sqs:DeleteMessage",
        "sqs:GetQueueAttributes",
      ]
      Resource = aws_sqs_queue.orders.arn
    }]
  })
}
```

## Alarmes CloudWatch
```hcl
# Lambda errors
resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  alarm_name          = "${local.full_name}-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 60
  statistic           = "Sum"
  threshold           = 0
  alarm_description   = "Lambda errors detected. Runbook: ${var.runbook_url}"
  alarm_actions       = [var.sns_alarm_topic_arn]
  dimensions = {
    FunctionName = aws_lambda_function.this.function_name
  }
  tags = local.common_tags
}

# DynamoDB throttling
resource "aws_cloudwatch_metric_alarm" "dynamo_throttle" {
  alarm_name          = "${var.service}-dynamodb-throttle-${var.environment}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "ThrottledRequests"
  namespace           = "AWS/DynamoDB"
  period              = 300
  statistic           = "Sum"
  threshold           = 0
  dimensions = {
    TableName = aws_dynamodb_table.orders.name
  }
  tags = local.common_tags
}
```

## Tags — Padrão obrigatório
```hcl
locals {
  common_tags = {
    Environment = var.environment
    Service     = var.service
    Team        = var.team
    ManagedBy   = "terraform"
    CostCenter  = var.cost_center
  }
}

# Aplicar em todo resource
resource "aws_dynamodb_table" "orders" {
  # ...
  tags = local.common_tags
}
```

## Checklist
- [ ] Remote state em S3 com encryption e DynamoDB lock?
- [ ] Módulos reutilizáveis para Lambda, SQS, DynamoDB?
- [ ] IAM com menor privilégio (sem `*`)?
- [ ] Tags obrigatórias em todos os recursos?
- [ ] Alarmes CloudWatch para cada componente?
- [ ] Lambda aliases (não `$LATEST`)?
- [ ] Encryption at rest (KMS) para dados sensíveis?
- [ ] `terraform fmt` e `terraform validate` em CI?
- [ ] `terraform plan` comentado em PRs?
- [ ] Variables com description e validation?
