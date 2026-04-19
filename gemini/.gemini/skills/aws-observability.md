# AWS Observability — CloudWatch, X-Ray & Alerting

Guia de observabilidade para workloads AWS.

## CloudWatch Logs

### Configuração Lambda
```hcl
resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${aws_lambda_function.handler.function_name}"
  retention_in_days = 30  # NUNCA deixar ilimitado — custo explode
  tags              = local.common_tags
}
```

### Structured logging (Python Lambda)
```python
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    logger.info(json.dumps({
        "message": "Processing order",
        "order_id": order_id,
        "request_id": context.aws_request_id,
        "function_version": context.function_version,
    }))
```

### Log Insights — Queries úteis
```sql
-- Erros nos últimos 30 minutos
fields @timestamp, @message
| filter @message like /ERROR/
| sort @timestamp desc
| limit 50

-- Latência p50, p95, p99 por endpoint
filter @type = "REPORT"
| stats avg(@duration) as p50,
        percentile(@duration, 95) as p95,
        percentile(@duration, 99) as p99
  by bin(5m)

-- Cold starts
filter @message like /Init Duration/
| stats count() as cold_starts by bin(1h)

-- Erros por mensagem
filter @message like /ERROR/
| stats count() by @message
| sort count desc
| limit 20
```

## CloudWatch Metrics & Alarms

### Métricas-chave por serviço

#### Lambda
| Métrica | Alarme quando |
|---------|-------------|
| `Errors` | > 0 (qualquer erro) |
| `Throttles` | > 0 (concorrência esgotada) |
| `Duration` | > 80% do timeout |
| `ConcurrentExecutions` | > 80% do reserved |

#### API Gateway
| Métrica | Alarme quando |
|---------|-------------|
| `5XXError` | > 1% das requests |
| `4XXError` | > 10% (pode indicar ataque) |
| `Latency` p99 | > SLO definido |
| `Count` | anomalia (spike/drop) |

#### SQS
| Métrica | Alarme quando |
|---------|-------------|
| `ApproximateNumberOfMessagesVisible` | > threshold (backlog) |
| `ApproximateAgeOfOldestMessage` | > threshold (lag) |
| `NumberOfMessagesSent` (DLQ) | > 0 |

#### DynamoDB
| Métrica | Alarme quando |
|---------|-------------|
| `ThrottledRequests` | > 0 |
| `SystemErrors` | > 0 |
| `ConsumedReadCapacityUnits` | > 80% provisioned |

### Terraform — Alarmes completos
```hcl
# Lambda error alarm
resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  alarm_name          = "${var.service}-lambda-errors-${var.environment}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = 60
  statistic           = "Sum"
  threshold           = 0
  treat_missing_data  = "notBreaching"
  alarm_description   = "Lambda errors. Runbook: ${var.runbook_url}"
  alarm_actions       = [var.sns_topic_arn]
  ok_actions          = [var.sns_topic_arn]
  dimensions = { FunctionName = var.function_name }
}

# SQS DLQ alarm (mensagens na DLQ = falha de processamento)
resource "aws_cloudwatch_metric_alarm" "dlq_messages" {
  alarm_name          = "${var.service}-dlq-messages-${var.environment}"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "ApproximateNumberOfMessagesVisible"
  namespace           = "AWS/SQS"
  period              = 60
  statistic           = "Sum"
  threshold           = 0
  alarm_description   = "Messages in DLQ. Investigate failed processing."
  alarm_actions       = [var.sns_topic_arn]
  dimensions = { QueueName = var.dlq_name }
}
```

## X-Ray / ADOT (Tracing)

### Habilitação Lambda
```hcl
resource "aws_lambda_function" "handler" {
  # ...
  tracing_config {
    mode = "Active"
  }
}

# IAM policy para X-Ray
resource "aws_iam_role_policy_attachment" "xray" {
  role       = aws_iam_role.lambda.name
  policy_arn = "arn:aws:iam::aws:policy/AWSXRayDaemonWriteAccess"
}
```

### Python com X-Ray SDK
```python
from aws_xray_sdk.core import xray_recorder, patch_all

patch_all()  # Auto-instrumenta boto3, requests, httplib

@xray_recorder.capture("process_order")
def process_order(order_id: str):
    # Subsegments automáticos para DynamoDB, SQS, etc.
    ...
```

## Dashboard — Template

```hcl
resource "aws_cloudwatch_dashboard" "service" {
  dashboard_name = "${var.service}-${var.environment}"
  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "metric"
        properties = {
          title   = "Lambda Invocations & Errors"
          metrics = [
            ["AWS/Lambda", "Invocations", "FunctionName", var.function_name],
            ["AWS/Lambda", "Errors", "FunctionName", var.function_name],
          ]
          period = 300
          stat   = "Sum"
        }
      },
      {
        type   = "metric"
        properties = {
          title   = "Lambda Duration (p50, p95, p99)"
          metrics = [
            ["AWS/Lambda", "Duration", "FunctionName", var.function_name, { stat = "p50" }],
            ["AWS/Lambda", "Duration", "FunctionName", var.function_name, { stat = "p95" }],
            ["AWS/Lambda", "Duration", "FunctionName", var.function_name, { stat = "p99" }],
          ]
          period = 300
        }
      },
      {
        type   = "metric"
        properties = {
          title   = "SQS Queue Depth"
          metrics = [
            ["AWS/SQS", "ApproximateNumberOfMessagesVisible", "QueueName", var.queue_name],
            ["AWS/SQS", "ApproximateNumberOfMessagesVisible", "QueueName", var.dlq_name],
          ]
        }
      }
    ]
  })
}
```

## Checklist
- [ ] Log groups com retention definido (não ilimitado)?
- [ ] Logs estruturados JSON com request_id e trace_id?
- [ ] Alarmes para Lambda: Errors, Throttles, Duration?
- [ ] Alarmes para SQS: DLQ, backlog, age?
- [ ] Alarmes para DynamoDB: throttles, system errors?
- [ ] X-Ray habilitado em Lambdas?
- [ ] Dashboard com métricas-chave do serviço?
- [ ] `alarm_description` com link para runbook?
- [ ] SNS topic configurado para notificações?
- [ ] Anomaly detection para métricas com padrão variável?
