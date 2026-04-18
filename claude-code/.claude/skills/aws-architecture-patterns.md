---
name: aws-architecture-patterns
description: "Padrões de arquitetura AWS: API Gateway + Lambda, SQS + Lambda, EventBridge, Step Functions, DynamoDB, S3. Use quando projetar solução AWS, escolher serviço, ou revisar arquitetura serverless."
---

# AWS Architecture Patterns

Padrões de arquitetura para AWS Serverless e serviços gerenciados.

## Padrão 1: API REST Serverless

```
Client → API Gateway → Lambda → DynamoDB
                     ↘ Lambda Authorizer (auth)
```

### Quando usar
- APIs com tráfego variável (pay-per-request)
- Baixa latência não é requisito crítico (cold start)
- Sem necessidade de WebSocket ou conexões longas

### Configuração
```hcl
# API Gateway
resource "aws_apigatewayv2_api" "api" {
  name          = "order-api"
  protocol_type = "HTTP"
}

# Lambda
resource "aws_lambda_function" "handler" {
  function_name = "order-handler"
  runtime       = "provided.al2023"
  handler       = "bootstrap"
  memory_size   = 256
  timeout       = 30

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.orders.name
    }
  }
}
```

## Padrão 2: Processamento assíncrono (SQS + Lambda)

```
Producer → SQS Queue → Lambda Consumer → DynamoDB
                 ↘ DLQ (após N falhas)
```

### Quando usar
- Processamento desacoplado
- Tolerância a latência (não precisa resposta imediata)
- Retry automático necessário

### Configuração essencial
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
            logger.error("Failed to process", message_id=record["messageId"], error=str(e))
            failures.append({"itemIdentifier": record["messageId"]})
    return {"batchItemFailures": failures}
```

## Padrão 3: Event-driven (EventBridge)

```
Service A → EventBridge → Rule 1 → Lambda A
                        → Rule 2 → Lambda B
                        → Rule 3 → SQS → Lambda C
```

### Quando usar
- Múltiplos consumers para o mesmo evento
- Desacoplamento entre producers e consumers
- Roteamento baseado em padrão de evento

### Evento padrão
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

### Regra com padrão
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

## Padrão 4: Workflow (Step Functions)

```
Step Functions:
  1. Validate Order → Lambda
  2. Check Inventory → Lambda
  3. Process Payment → Lambda
  4. (if payment failed) → Compensate → Lambda
  5. Send Notification → SNS
```

### Quando usar
- Fluxo com múltiplos passos e decisões
- Necessidade de compensação (saga pattern)
- Visibilidade do estado do workflow
- Timeout longo (até 1 ano)

### Quando NÃO usar
- Fluxo simples (A → B) → SQS + Lambda basta
- Latência crítica → Step Functions adiciona overhead
- Alto volume (>1000/s) → custo pode ser proibitivo

## Padrão 5: DynamoDB — Modelagem

### Single-table design
```
PK              SK                   Attributes
ORDER#123       METADATA             status, total, createdAt
ORDER#123       ITEM#prod-1          quantity, price
ORDER#123       PAYMENT#txn-456      amount, status
CUSTOMER#789    PROFILE              name, email
CUSTOMER#789    ORDER#123            total, status (GSI para listar orders por customer)
```

### Regras
- PK + SK devem suportar todos os access patterns
- GSI para access patterns secundários
- Evitar scan — sempre query
- Capacity: on-demand para tráfego imprevisível, provisioned para estável
- TTL para dados temporários (sessões, cache, tokens)

## Padrão 6: S3 + Event → Lambda

```
S3 Bucket → Event Notification → SQS → Lambda → Processed Output
```

### Quando usar
- Processamento de arquivos (CSV, JSON, imagens)
- ETL de dados
- Sempre usar SQS entre S3 e Lambda (evita perda de eventos)

## Decisão: Lambda vs ECS/Fargate

| Critério | Lambda | ECS/Fargate |
|----------|--------|-------------|
| Tráfego | Variável, spiky | Constante, previsível |
| Latência | Tolerante a cold start | Submilissegundo necessário |
| Duração | < 15 min | Longo (horas/dias) |
| Memória | < 10 GB | Ilimitada (praticamente) |
| WebSocket | Não | Sim |
| Custo (baixo tráfego) | Menor | Maior |
| Custo (alto tráfego constante) | Maior | Menor |
| Operação | Menor (serverless) | Maior (containers) |

## Checklist de arquitetura AWS
- [ ] Serviço correto para o caso de uso?
- [ ] IAM com menor privilégio?
- [ ] VPC quando necessário (RDS), não quando desnecessário (DynamoDB)?
- [ ] Encryption at rest e in transit?
- [ ] Alarmes CloudWatch para cada componente?
- [ ] DLQ para processamento assíncrono?
- [ ] Idempotência implementada?
- [ ] Retry com backoff em chamadas entre serviços?
- [ ] Tags de custo em todos os recursos?
- [ ] Logs centralizados e estruturados?
- [ ] Multi-AZ para componentes críticos?
