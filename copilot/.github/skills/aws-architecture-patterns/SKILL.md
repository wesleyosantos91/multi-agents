---
name: aws-architecture-patterns
description: Skill importada do EXEMPLO (aws-architecture-patterns.md).
allowed-tools: "read,search"
user-invocable: true
---

# Skill

---
name: aws-architecture-patterns
description: "Padrões de arquitetura AWS: API Gateway + Lambda, SQS + Lambda, EventBridge, Step Functions, DynamoDB, S3, ECS/Fargate, ElastiCache, CloudFront, SAM, CDK, Lambda Layers, cold start, SnapStart. Use quando projetar solução AWS, escolher serviço, ou revisar arquitetura."
---

# AWS Architecture Patterns — Serverless

Padroes de arquitetura para AWS Serverless e servicos gerenciados.

## Padrao 1: API REST Serverless

```
Client → API Gateway → Lambda → DynamoDB
                     ↘ Lambda Authorizer (auth)
```

### Quando usar
- APIs com trafego variavel (pay-per-request)
- Baixa latencia nao e requisito critico (cold start)
- Sem necessidade de WebSocket ou conexoes longas

### Configuracao
```hcl
resource "aws_apigatewayv2_api" "api" {
  name          = "order-api"
  protocol_type = "HTTP"
}

resource "aws_lambda_function" "handler" {
  function_name = "order-handler"
  runtime       = "provided.al2023"
  handler       = "bootstrap"
  memory_size   = 256
  timeout       = 30
  layers        = [aws_lambda_layer_version.common.arn]

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.orders.name
    }
  }
}
```

## Padrao 2: Processamento assincrono (SQS + Lambda)

```
Producer → SQS Queue → Lambda Consumer → DynamoDB
                 ↘ DLQ (apos N falhas)
```

### Quando usar
- Processamento desacoplado
- Tolerancia a latencia (nao precisa resposta imediata)
- Retry automatico necessario

### Configuracao essencial
```hcl
resource "aws_sqs_queue" "orders" {
  name                       = "order-processing"
  visibility_timeout_seconds = 180  # 6x o timeout da Lambda
  receive_wait_time_seconds  = 20   # long polling
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.orders_dlq.arn
    maxReceiveCount     = 3
  })
}

resource "aws_lambda_event_source_mapping" "sqs" {
  event_source_arn                   = aws_sqs_queue.orders.arn
  function_name                      = aws_lambda_function.consumer.arn
  batch_size                         = 10
  maximum_batching_window_in_seconds = 5
  function_response_types            = ["ReportBatchItemFailures"]
}
```

### ReportBatchItemFailures (parcial)
```python
def handler(event, context):
    failures = []
    for record in event["Records"]:
        try:
            process(json.loads(record["body"]))
        except Exception as e:
            logger.error("Failed", message_id=record["messageId"], error=str(e))
            failures.append({"itemIdentifier": record["messageId"]})
    return {"batchItemFailures": failures}
```

## Padrao 3: Event-driven (EventBridge)

```
Service A → EventBridge → Rule 1 → Lambda A
                        → Rule 2 → Lambda B
                        → Rule 3 → SQS → Lambda C
```

### Quando usar
- Multiplos consumers para o mesmo evento
- Desacoplamento entre producers e consumers
- Roteamento baseado em padrao de evento

### Evento padrao
```json
{
  "source": "order-service",
  "detail-type": "OrderCreated",
  "detail": {
    "orderId": "ord-123",
    "customerId": "cust-456",
    "total": 150.00
  }
}
```

### Regra com padrao
```hcl
resource "aws_cloudwatch_event_rule" "high_value_orders" {
  name = "high-value-orders"
  event_pattern = jsonencode({
    source      = ["order-service"]
    detail-type = ["OrderCreated"]
    detail = {
      total = [{ numeric = [">=", 1000] }]
    }
  })
}
```

## Padrao 4: Workflow (Step Functions)

```
Step Functions:
  1. Validate Order → Lambda
  2. Check Inventory → Lambda
  3. Process Payment → Lambda
  4. (if failed) → Compensate → Lambda
  5. Send Notification → SNS
```

### Quando usar
- Fluxo com multiplos passos e decisoes
- Saga pattern (compensacao)
- Timeout longo (ate 1 ano)

### Quando NAO usar
- Fluxo simples (A → B) → SQS + Lambda basta
- Latencia critica → overhead de Step Functions
- Alto volume (>1000/s) → custo proibitivo

## Padrao 5: DynamoDB — Modelagem

### Single-table design
```
PK              SK                   Attributes
ORDER#123       METADATA             status, total, createdAt
ORDER#123       ITEM#prod-1          quantity, price
ORDER#123       PAYMENT#txn-456      amount, status
CUSTOMER#789    PROFILE              name, email
CUSTOMER#789    ORDER#123            total, status (GSI)
```

### Regras
- PK + SK devem suportar todos os access patterns
- GSI para access patterns secundarios
- Evitar scan — sempre query
- On-demand para trafego imprevisivel, provisioned para estavel
- TTL para dados temporarios

## Padrao 6: S3 + Event → Lambda

```
S3 Bucket → Event Notification → SQS → Lambda → Output
```

- Processamento de arquivos (CSV, JSON, imagens)
- Sempre usar SQS entre S3 e Lambda (evita perda de eventos)

## Serverless Framework — SAM vs CDK vs Terraform

| Criterio | SAM | CDK | Terraform |
|----------|-----|-----|-----------|
| Linguagem | YAML | TypeScript/Python/Java | HCL |
| Escopo | Lambda-focused | AWS completo | Multi-cloud |
| Local testing | `sam local invoke` | — | — |
| Deploy | `sam deploy` | `cdk deploy` | `terraform apply` |
| Curva | Baixa | Media | Media |
| Melhor para | PoC, Lambda puro | Apps AWS complexas | Multi-cloud, IaC existente |

### SAM template
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Timeout: 30
    Runtime: java21
    MemorySize: 512
    Architectures: [arm64]
    Environment:
      Variables:
        TABLE_NAME: !Ref OrderTable

Resources:
  OrderApi:
    Type: AWS::Serverless::Function
    Properties:
      Handler: com.example.Handler::handleRequest
      Events:
        GetOrders:
          Type: Api
          Properties:
            Path: /orders
            Method: get
        CreateOrder:
          Type: Api
          Properties:
            Path: /orders
            Method: post

  OrderTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: orders
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: id
          AttributeType: S
      KeySchema:
        - AttributeName: id
          KeyType: HASH
```

## Lambda Layers

```hcl
# Layer compartilhada entre Lambdas
resource "aws_lambda_layer_version" "common" {
  layer_name          = "common-deps"
  compatible_runtimes = ["java21"]
  filename            = "layers/common-deps.zip"
  description         = "Shared dependencies: AWS SDK, logging, utils"
}

# Uso
resource "aws_lambda_function" "handler" {
  layers = [aws_lambda_layer_version.common.arn]
}
```

### Quando usar Layers
- Dependencias compartilhadas entre multiplas Lambdas
- Reduzir tamanho do deployment package
- Separar codigo de negocio de dependencias

### Quando NAO usar
- Uma unica Lambda — embed tudo
- Layers muito grandes (>50MB) — considere container image

## Cold Start — Mitigacao

| Estrategia | Linguagem | Reducao |
|------------|-----------|---------|
| **SnapStart** | Java (Corretto) | ~90% (snapshot de memoria) |
| **Provisioned Concurrency** | Todas | Elimina cold start |
| **ARM64 (Graviton)** | Todas | ~10-20% + custo menor |
| **Menor package size** | Todas | Proporcional |
| **GraalVM Native** | Java (Quarkus/Micronaut) | ~95% |
| **Init fora do handler** | Todas | SDK clients, conexoes |

```hcl
# SnapStart (Java)
resource "aws_lambda_function" "handler" {
  runtime = "java21"
  snap_start { apply_on = "PublishedVersions" }
}

# Provisioned Concurrency
resource "aws_lambda_provisioned_concurrency_config" "main" {
  function_name                  = aws_lambda_function.handler.function_name
  qualifier                      = aws_lambda_alias.prod.name
  provisioned_concurrent_executions = 5
}

# ARM64 (Graviton) — 20% mais barato
resource "aws_lambda_function" "handler" {
  architectures = ["arm64"]
}
```

## Padrao 7: ECS/Fargate — Container Services

```
Client → ALB → ECS Service (Fargate) → DynamoDB/RDS
                    ↕ Service Discovery (Cloud Map)
              Auto Scaling (target tracking)
```

### Quando usar (em vez de Lambda)
- Trafego constante e previsivel
- Latencia submilissegundo necessaria
- Processos long-running (>15 min)
- WebSocket, gRPC streaming, conexoes persistentes
- Aplicacao com estado em memoria (cache local)

### Task Definition
```hcl
resource "aws_ecs_task_definition" "app" {
  family                   = "${var.service}-${var.environment}"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = var.cpu     # 256, 512, 1024, 2048, 4096
  memory                   = var.memory  # 512, 1024, 2048, ...
  execution_role_arn       = aws_iam_role.ecs_execution.arn
  task_role_arn            = aws_iam_role.ecs_task.arn

  container_definitions = jsonencode([{
    name  = var.service
    image = "${var.ecr_repo}:${var.image_tag}"
    portMappings = [{ containerPort = 8080, protocol = "tcp" }]
    environment = [
      { name = "ENV", value = var.environment },
      { name = "TABLE_NAME", value = var.dynamodb_table },
    ]
    secrets = [
      { name = "DB_PASSWORD", valueFrom = aws_secretsmanager_secret.db.arn },
    ]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = aws_cloudwatch_log_group.app.name
        "awslogs-region"        = var.region
        "awslogs-stream-prefix" = var.service
      }
    }
    healthCheck = {
      command     = ["CMD-SHELL", "curl -f http://localhost:8080/actuator/health || exit 1"]
      interval    = 30
      timeout     = 5
      retries     = 3
      startPeriod = 60
    }
  }])

  tags = local.common_tags
}
```

### Service + ALB
```hcl
resource "aws_ecs_service" "app" {
  name            = var.service
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.app.arn
  desired_count   = var.min_capacity
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.private_subnet_ids
    security_groups  = [aws_security_group.ecs.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.app.arn
    container_name   = var.service
    container_port   = 8080
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  deployment_configuration {
    maximum_percent         = 200
    minimum_healthy_percent = 100
  }
}

# Auto Scaling
resource "aws_appautoscaling_target" "ecs" {
  max_capacity       = var.max_capacity
  min_capacity       = var.min_capacity
  resource_id        = "service/${aws_ecs_cluster.main.name}/${aws_ecs_service.app.name}"
  scalable_dimension = "ecs:service:DesiredCount"
  service_namespace  = "ecs"
}

resource "aws_appautoscaling_policy" "cpu" {
  name               = "${var.service}-cpu-scaling"
  policy_type        = "TargetTrackingScaling"
  resource_id        = aws_appautoscaling_target.ecs.resource_id
  scalable_dimension = aws_appautoscaling_target.ecs.scalable_dimension
  service_namespace  = aws_appautoscaling_target.ecs.service_namespace

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "ECSServiceAverageCPUUtilization"
    }
    target_value       = 70.0
    scale_in_cooldown  = 300
    scale_out_cooldown = 60
  }
}
```

## Padrao 8: Caching (ElastiCache + DAX + CloudFront)

### ElastiCache Redis — Session/Data cache
```hcl
resource "aws_elasticache_replication_group" "cache" {
  replication_group_id = "${var.service}-cache-${var.environment}"
  description          = "Redis cache for ${var.service}"
  node_type            = var.environment == "prod" ? "cache.r7g.large" : "cache.t4g.micro"
  num_cache_clusters   = var.environment == "prod" ? 2 : 1  # Multi-AZ em prod
  engine_version       = "7.1"
  port                 = 6379
  subnet_group_name    = aws_elasticache_subnet_group.cache.name
  security_group_ids   = [aws_security_group.cache.id]
  at_rest_encryption_enabled = true
  transit_encryption_enabled = true
  automatic_failover_enabled = var.environment == "prod"
  tags                 = local.common_tags
}
```

### DAX — DynamoDB Accelerator
```hcl
resource "aws_dax_cluster" "orders" {
  cluster_name       = "${var.service}-dax-${var.environment}"
  node_type          = "dax.t3.small"
  replication_factor = var.environment == "prod" ? 3 : 1
  iam_role_arn       = aws_iam_role.dax.arn
  subnet_group_name  = aws_dax_subnet_group.main.name
  security_group_ids = [aws_security_group.dax.id]
  tags               = local.common_tags
}
```

### CloudFront — CDN + API caching
```hcl
resource "aws_cloudfront_distribution" "api" {
  origin {
    domain_name = aws_lb.app.dns_name
    origin_id   = "alb"
    custom_origin_config {
      http_port              = 80
      https_port             = 443
      origin_protocol_policy = "https-only"
      origin_ssl_protocols   = ["TLSv1.2"]
    }
  }

  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD", "OPTIONS", "PUT", "POST", "PATCH", "DELETE"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "alb"
    viewer_protocol_policy = "redirect-to-https"
    cache_policy_id        = aws_cloudfront_cache_policy.api.id

    function_association {
      event_type   = "viewer-request"
      function_arn = aws_cloudfront_function.security_headers.arn
    }
  }

  restrictions { geo_restriction { restriction_type = "none" } }
  viewer_certificate { cloudfront_default_certificate = true }
  tags = local.common_tags
}
```

### Quando usar cada tipo de cache

| Tipo | Quando | Latencia |
|------|--------|----------|
| **DAX** | DynamoDB read-heavy, microsegundos | ~1ms |
| **ElastiCache Redis** | Session, data cache, pub/sub, rate limiting | ~1-5ms |
| **CloudFront** | Assets estaticos, API responses cacheáveis | Edge (global) |
| **API Gateway cache** | Responses REST cacheáveis por path+params | Regional |
| **Application cache** | In-process, hot data, lookup tables | ~0ms |

### Cache invalidation patterns
- **TTL-based**: simples, eventual consistency (maioria dos casos)
- **Write-through**: atualiza cache junto com banco (consistencia forte)
- **Write-behind**: atualiza cache, persiste async (performance, risco de perda)
- **Event-driven**: DynamoDB Streams/EventBridge invalida cache no write

## Lambda vs ECS/Fargate

| Criterio | Lambda | ECS/Fargate |
|----------|--------|-------------|
| Trafego | Variavel, spiky | Constante, previsivel |
| Latencia | Tolerante a cold start | Submilissegundo |
| Duracao | < 15 min | Longo (horas/dias) |
| Memoria | < 10 GB | Ilimitada |
| WebSocket | Nao | Sim |
| Custo (baixo trafego) | Menor | Maior |
| Custo (alto trafego) | Maior | Menor |
| Operacao | Menor (serverless) | Maior (containers) |

## Checklist

- [ ] Servico correto para o caso de uso (Lambda vs ECS)?
- [ ] IAM com menor privilegio?
- [ ] VPC quando necessario (RDS), nao quando desnecessario (DynamoDB)?
- [ ] Encryption at rest e in transit?
- [ ] Alarmes CloudWatch para cada componente?
- [ ] DLQ para processamento assincrono?
- [ ] Idempotencia implementada?
- [ ] Retry com backoff em chamadas entre servicos?
- [ ] Tags de custo em todos os recursos?
- [ ] Logs centralizados e estruturados?
- [ ] Multi-AZ para componentes criticos?
- [ ] Cold start mitigado (SnapStart, Provisioned, ARM64)?
- [ ] Lambda Layers para deps compartilhadas?
- [ ] SAM/CDK/Terraform escolhido e padronizado?
