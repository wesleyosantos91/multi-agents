---
name: aws-iac-patterns
description: Skill importada do EXEMPLO (aws-iac-patterns.md).
allowed-tools: "read,search"
user-invocable: true
---

# Skill

---
name: aws-iac-patterns
description: "Padrões de IaC AWS com Terraform: módulos, remote state, IAM, networking, secrets management (Secrets Manager, Parameter Store, rotation), ambiente multi-env. Use quando configurar infra AWS, criar módulos Terraform, gerenciar secrets ou revisar IaC AWS."
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

## Secrets Management

### Secrets Manager vs Parameter Store

| Criterio | Secrets Manager | Parameter Store |
|----------|----------------|-----------------|
| Rotacao automatica | Nativo | Manual (Lambda custom) |
| Custo | $0.40/secret/mes + API calls | Free (standard), $0.05/param (advanced) |
| Cross-account | Sim (resource policy) | Nao |
| Tamanho max | 64 KB | 8 KB (advanced) |
| Melhor para | Credenciais BD, API keys, certificados | Config, feature flags, endpoints |

### Secrets Manager — Terraform
```hcl
resource "aws_secretsmanager_secret" "db_credentials" {
  name                    = "${var.service}/${var.environment}/db-credentials"
  description             = "Database credentials for ${var.service}"
  recovery_window_in_days = var.environment == "prod" ? 30 : 7
  tags                    = local.common_tags
}

resource "aws_secretsmanager_secret_version" "db_credentials" {
  secret_id = aws_secretsmanager_secret.db_credentials.id
  secret_string = jsonencode({
    username = var.db_username
    password = var.db_password
    host     = aws_db_instance.main.address
    port     = aws_db_instance.main.port
    dbname   = var.db_name
  })
}
```

### Rotacao automatica
```hcl
resource "aws_secretsmanager_secret_rotation" "db_credentials" {
  secret_id           = aws_secretsmanager_secret.db_credentials.id
  rotation_lambda_arn = aws_lambda_function.secret_rotation.arn
  rotation_rules {
    automatically_after_days = 30
  }
}

# Lambda de rotacao
resource "aws_lambda_function" "secret_rotation" {
  function_name = "${var.service}-secret-rotation-${var.environment}"
  runtime       = "python3.13"
  handler       = "rotation.handler"
  timeout       = 30
  role          = aws_iam_role.rotation_lambda.arn

  environment {
    variables = {
      SECRET_ARN = aws_secretsmanager_secret.db_credentials.arn
    }
  }
}

# Permissao para Secrets Manager invocar a Lambda
resource "aws_lambda_permission" "secretsmanager" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.secret_rotation.function_name
  principal     = "secretsmanager.amazonaws.com"
  source_arn    = aws_secretsmanager_secret.db_credentials.arn
}
```

### Parameter Store — Terraform
```hcl
# Parametro simples (free tier)
resource "aws_ssm_parameter" "api_endpoint" {
  name        = "/${var.service}/${var.environment}/api-endpoint"
  type        = "String"
  value       = var.api_endpoint
  description = "External API endpoint for ${var.service}"
  tags        = local.common_tags
}

# Parametro sensivel (encrypted)
resource "aws_ssm_parameter" "api_key" {
  name        = "/${var.service}/${var.environment}/api-key"
  type        = "SecureString"
  value       = var.api_key
  key_id      = aws_kms_key.main.arn
  description = "External API key"
  tags        = local.common_tags
}
```

### IAM para Lambda acessar secrets
```hcl
resource "aws_iam_policy" "read_secrets" {
  name = "${local.full_name}-read-secrets"
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = ["secretsmanager:GetSecretValue"]
        Resource = [aws_secretsmanager_secret.db_credentials.arn]
      },
      {
        Effect = "Allow"
        Action = ["ssm:GetParameter", "ssm:GetParametersByPath"]
        Resource = ["arn:aws:ssm:${var.region}:${data.aws_caller_identity.current.account_id}:parameter/${var.service}/${var.environment}/*"]
      },
      {
        Effect   = "Allow"
        Action   = ["kms:Decrypt"]
        Resource = [aws_kms_key.main.arn]
      },
    ]
  })
}
```

### Leitura em runtime

```java
// Java — AWS SDK + cache
@Configuration
public class SecretsConfig {
    @Bean
    @Profile("!test")
    public DatabaseCredentials databaseCredentials(SecretsManagerClient client) {
        var response = client.getSecretValue(b -> b.secretId("order-service/prod/db-credentials"));
        return objectMapper.readValue(response.secretString(), DatabaseCredentials.class);
    }
}
```

```python
# Python — boto3 + cache
import boto3, json
from functools import lru_cache

@lru_cache(maxsize=1)
def get_db_credentials() -> dict:
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=f"{SERVICE}/{ENV}/db-credentials")
    return json.loads(response["SecretString"])
```

```go
// Go — AWS SDK v2
func GetSecret(ctx context.Context, client *secretsmanager.Client, secretID string) (map[string]string, error) {
    output, err := client.GetSecretValue(ctx, &secretsmanager.GetSecretValueInput{
        SecretId: &secretID,
    })
    if err != nil {
        return nil, fmt.Errorf("getting secret %s: %w", secretID, err)
    }
    var result map[string]string
    if err := json.Unmarshal([]byte(*output.SecretString), &result); err != nil {
        return nil, fmt.Errorf("parsing secret: %w", err)
    }
    return result, nil
}
```

### Regras de secrets
- **Nunca** hardcoded em codigo, env vars de CI, ou terraform.tfvars commitados
- Secrets Manager para credenciais que rotacionam
- Parameter Store SecureString para config sensivel estatica
- KMS customer-managed key para encryption
- IAM com menor privilegio (secret ARN especifico)
- Cache em runtime (evitar chamadas repetidas)
- Rotacao automatica para credenciais de banco

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
- [ ] Secrets em Secrets Manager (nao env vars ou tfvars)?
- [ ] Rotacao automatica para credenciais de banco?
- [ ] Parameter Store para config sensivel estatica?
- [ ] IAM restrito a secrets especificos (nao `*`)?
