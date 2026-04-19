---
name: async-messaging-patterns
description: "Padrões de mensageria assíncrona e event-driven: SQS, SNS, Kafka, EventBridge, idempotência, DLQ, ordering, retry. Use quando implementar consumers, producers ou arquitetura event-driven."
argument-hint: "[contexto adicional]"
---

# Async Messaging — Patterns & Idioms

Padroes para mensageria assincrona e arquiteturas event-driven em producao.

## Escolha de tecnologia

| Criterio | SQS | SNS+SQS | Kafka | EventBridge |
|----------|-----|---------|-------|-------------|
| Point-to-point | Sim | — | — | — |
| Fan-out (1→N) | — | Sim | Sim (consumer groups) | Sim (rules) |
| Ordering | FIFO (por group) | FIFO | Sim (por partition) | Nao garantido |
| Replay | Nao | Nao | Sim (retention) | Archive+Replay |
| Throughput | Alto | Alto | Muito alto | Moderado |
| Latencia | ~ms | ~ms | ~ms | ~50-100ms |
| Serverless native | Sim (Lambda trigger) | Sim | Nao (MSK) | Sim |
| Custo em idle | Zero | Zero | Fixo (brokers) | Zero |

## Estrutura de evento

```json
{
  "eventId": "evt-abc123",
  "eventType": "order.created",
  "eventVersion": "1.0",
  "source": "order-service",
  "timestamp": "2026-04-18T10:30:00Z",
  "correlationId": "req-xyz789",
  "data": {
    "orderId": "ord-456",
    "customerId": "cust-789",
    "amount": 299.90,
    "status": "pending"
  },
  "metadata": {
    "traceId": "trace-abc",
    "environment": "production"
  }
}
```

### Regras de design de eventos

- **eventId**: UUID unico por evento — essencial para idempotencia
- **eventType**: `<domain>.<action>` em past tense (`order.created`, nao `create.order`)
- **eventVersion**: versionamento explicito do schema
- **correlationId**: rastrear fluxo end-to-end
- **data**: payload do evento — nao incluir dados sensiveis
- Eventos sao **fatos imutaveis** — nao comandos

## Idempotencia (obrigatorio)

Todo consumer DEVE ser idempotente. Mensagens podem ser entregues mais de uma vez.

```java
// Java — Idempotency com DynamoDB
@Service
public class IdempotentProcessor {

    private final DynamoDbTable<ProcessedEvent> table;

    public boolean tryProcess(String eventId, Runnable action) {
        try {
            table.putItem(PutItemEnhancedRequest.builder(ProcessedEvent.class)
                .item(new ProcessedEvent(eventId, Instant.now()))
                .conditionExpression(Expression.builder()
                    .expression("attribute_not_exists(eventId)")
                    .build())
                .build());

            action.run();
            return true;
        } catch (ConditionalCheckFailedException e) {
            log.info("Event already processed: {}", eventId);
            return false; // idempotente — nao reprocessar
        }
    }
}
```

```python
# Python — Idempotency com powertools
from aws_lambda_powertools.utilities.idempotency import (
    idempotent, DynamoDBPersistenceLayer, IdempotencyConfig,
)

persistence = DynamoDBPersistenceLayer(table_name="idempotency")
config = IdempotencyConfig(event_key_jmespath="detail.eventId", expires_after_seconds=3600)

@idempotent(config=config, persistence_store=persistence)
def process_order(event):
    order_id = event["detail"]["data"]["orderId"]
    order_service.process(order_id)
```

```go
// Go — Idempotency check
func (p *Processor) Process(ctx context.Context, event Event) error {
    processed, err := p.idempotencyStore.Exists(ctx, event.EventID)
    if err != nil { return fmt.Errorf("idempotency check: %w", err) }
    if processed { return nil }

    if err := p.service.Handle(ctx, event); err != nil { return err }

    return p.idempotencyStore.Mark(ctx, event.EventID)
}
```

## SQS + Lambda

```java
// Java — SQS Lambda handler com partial batch failure
public class OrderSqsHandler implements RequestHandler<SQSEvent, SQSBatchResponse> {

    @Override
    public SQSBatchResponse handleRequest(SQSEvent event, Context context) {
        var failures = new ArrayList<SQSBatchResponse.BatchItemFailure>();

        for (var record : event.getRecords()) {
            try {
                var orderEvent = objectMapper.readValue(record.getBody(), OrderEvent.class);
                idempotentProcessor.tryProcess(orderEvent.eventId(),
                    () -> orderService.process(orderEvent));
            } catch (Exception e) {
                log.error("Failed to process message: {}", record.getMessageId(), e);
                failures.add(new SQSBatchResponse.BatchItemFailure(record.getMessageId()));
            }
        }

        return new SQSBatchResponse(failures);
    }
}
```

```yaml
# SAM/CloudFormation
OrderFunction:
  Type: AWS::Serverless::Function
  Properties:
    Events:
      SQSEvent:
        Type: SQS
        Properties:
          Queue: !GetAtt OrderQueue.Arn
          BatchSize: 10
          MaximumBatchingWindowInSeconds: 5
          FunctionResponseTypes:
            - ReportBatchItemFailures  # Partial batch failure
```

## Kafka (consumer)

```java
// Java — Spring Kafka consumer
@Component
public class OrderKafkaConsumer {

    @KafkaListener(
        topics = "orders",
        groupId = "order-processor",
        containerFactory = "kafkaListenerContainerFactory",
    )
    public void consume(
        @Payload String payload,
        @Header(KafkaHeaders.RECEIVED_KEY) String key,
        @Header("eventId") String eventId,
        Acknowledgment ack
    ) {
        try {
            var event = objectMapper.readValue(payload, OrderEvent.class);
            if (idempotentProcessor.tryProcess(eventId, () -> orderService.process(event))) {
                ack.acknowledge();
            } else {
                ack.acknowledge(); // ja processado — commit offset
            }
        } catch (Exception e) {
            log.error("Failed to process event: {}", eventId, e);
            // NAO acknowledge — retry automatico
            throw e;
        }
    }
}
```

```go
// Go — Kafka consumer
func (c *Consumer) Run(ctx context.Context) error {
    for {
        msg, err := c.reader.ReadMessage(ctx)
        if err != nil {
            if errors.Is(err, context.Canceled) { return nil }
            return fmt.Errorf("read message: %w", err)
        }

        var event OrderEvent
        if err := json.Unmarshal(msg.Value, &event); err != nil {
            slog.Error("invalid message", "error", err, "offset", msg.Offset)
            continue // skip poison message
        }

        if err := c.processor.Process(ctx, event); err != nil {
            slog.Error("process failed", "error", err, "eventId", event.EventID)
            // decidir: retry, DLQ, ou skip
        }
    }
}
```

## EventBridge

```java
// Producer
public class OrderEventPublisher {
    private final EventBridgeClient eventBridge;

    public void publish(OrderEvent event) {
        eventBridge.putEvents(PutEventsRequest.builder()
            .entries(PutEventsRequestEntry.builder()
                .source("order-service")
                .detailType("order.created")
                .detail(objectMapper.writeValueAsString(event))
                .eventBusName("orders")
                .build())
            .build());
    }
}
```

```python
# Consumer — Lambda triggered by EventBridge rule
def handler(event, context):
    detail = event["detail"]
    event_id = detail["eventId"]
    order_id = detail["data"]["orderId"]

    logger.info("processing", event_id=event_id, order_id=order_id)
    order_service.process(detail)
```

## Retry com backoff e jitter

```yaml
# SQS Redrive Policy
OrderQueue:
  Type: AWS::SQS::Queue
  Properties:
    VisibilityTimeout: 300  # 5x o timeout da Lambda
    RedrivePolicy:
      deadLetterTargetArn: !GetAtt OrderDLQ.Arn
      maxReceiveCount: 3    # 3 tentativas antes de DLQ

OrderDLQ:
  Type: AWS::SQS::Queue
  Properties:
    MessageRetentionPeriod: 1209600  # 14 dias
```

```java
// Retry com exponential backoff + jitter (client-side)
@Retryable(
    maxAttempts = 3,
    backoff = @Backoff(delay = 1000, multiplier = 2, maxDelay = 10000, random = true)
)
public void publishEvent(OrderEvent event) {
    eventBridge.putEvents(/* ... */);
}
```

## DLQ e poison message handling

```python
# Lambda para processar DLQ (investigacao/reprocessamento)
def dlq_handler(event, context):
    for record in event["Records"]:
        body = json.loads(record["body"])
        logger.warning("DLQ message",
            event_id=body.get("eventId"),
            error=record.get("attributes", {}).get("DeadLetterQueueSourceArn"),
            receive_count=record["attributes"]["ApproximateReceiveCount"],
        )
        # Opcoes: alertar, salvar para analise, reprocessar, descartar
        metrics.increment("dlq.messages.received", tags={"source": body.get("source")})
```

## Schema evolution

| Estrategia | Descricao | Quando |
|------------|-----------|--------|
| **Additive** | Adicionar campos novos (nullable/default) | Sempre preferido |
| **Versioned** | Novo eventType com versao (`order.created.v2`) | Breaking change necessario |
| **Schema Registry** | Avro/Protobuf com compatibilidade BACKWARD | Kafka com contratos fortes |

```python
# Additive — novo campo com default
# v1: {"orderId": "...", "amount": 99.0}
# v2: {"orderId": "...", "amount": 99.0, "currency": "BRL"}  # novo campo

# Consumer tolerante
currency = event.get("currency", "BRL")  # default para backward compat
```

## Observabilidade

```java
// Metricas essenciais
// - messages.received (counter)
// - messages.processed (counter, tag: success/failure)
// - messages.processing_time (histogram)
// - messages.dlq (counter)
// - consumer.lag (gauge) — Kafka
// - queue.depth (gauge) — SQS ApproximateNumberOfMessages

// Tracing — propagar trace ID
var traceId = event.metadata().traceId();
Span span = tracer.spanBuilder("process-order")
    .setParent(Context.current().with(extractTraceContext(traceId)))
    .startSpan();
```

## Checklist

- [ ] Idempotencia em todo consumer?
- [ ] Partial batch failure (ReportBatchItemFailures)?
- [ ] DLQ configurada com retention adequada?
- [ ] Retry com backoff exponencial + jitter?
- [ ] Poison message handling (nao bloquear fila)?
- [ ] Ordering garantido quando necessario (FIFO/partition key)?
- [ ] Event schema versionado e documentado?
- [ ] Correlation ID propagado end-to-end?
- [ ] Metricas: processed, failed, lag, DLQ depth?
- [ ] Tracing distribuido entre producer e consumer?
- [ ] VisibilityTimeout >= 5x Lambda timeout?
- [ ] Schema evolution backward-compatible?
