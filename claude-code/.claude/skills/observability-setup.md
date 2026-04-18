---
name: observability-setup
description: "Configura ou revisa observabilidade: logs estruturados, métricas e tracing. Use quando pedirem para adicionar logging, métricas, tracing ou observabilidade."
---

# Observability Setup

Configure os 3 pilares de observabilidade: logs, métricas e tracing.

## 1. Logs estruturados

### Regras
- JSON em produção — nunca texto livre
- Campos obrigatórios: `timestamp`, `level`, `message`, `service`, `traceId`
- Sem dados sensíveis (PII, senhas, tokens) em logs
- Log no nível correto:
  - `ERROR`: falha que impacta funcionalidade
  - `WARN`: situação inesperada mas recuperável
  - `INFO`: eventos de negócio relevantes (pedido criado, pagamento processado)
  - `DEBUG`: detalhes técnicos para troubleshooting (não em produção)

### Exemplo de log estruturado
```json
{
  "timestamp": "2024-01-15T10:30:00.123Z",
  "level": "INFO",
  "message": "Order created successfully",
  "service": "order-api",
  "traceId": "abc-123-def",
  "orderId": "ord-456",
  "customerId": "cust-789",
  "amount": 150.00,
  "duration_ms": 45
}
```

## 2. Métricas

### Métricas obrigatórias
- **Request rate**: requisições por segundo por endpoint
- **Error rate**: taxa de erros (4xx, 5xx) por endpoint
- **Latency**: p50, p95, p99 por endpoint
- **Saturation**: CPU, memória, conexões, threads/goroutines

### RED Method (para serviços)
- **R**ate: quantas requisições por segundo?
- **E**rrors: quantas falham?
- **D**uration: quanto tempo levam?

### USE Method (para recursos)
- **U**tilization: quanto do recurso está sendo usado?
- **S**aturation: há fila/backpressure?
- **E**rrors: há erros no recurso?

## 3. Tracing distribuído

### Regras
- Propagar `traceId` entre serviços (headers HTTP, message headers)
- Criar spans para operações significativas (chamadas externas, queries, processamento)
- Não criar spans para operações triviais (getters, validações simples)
- Incluir `traceId` nos logs para correlação

### Instrumentação
- Java: OpenTelemetry Java Agent (auto-instrumentation)
- Python: OpenTelemetry Python SDK
- Go: OpenTelemetry Go SDK
- AWS Lambda: AWS X-Ray ou ADOT (AWS Distro for OpenTelemetry)

## Checklist
- [ ] Logs em JSON em produção?
- [ ] Campos obrigatórios presentes (timestamp, level, message, service, traceId)?
- [ ] Sem PII em logs?
- [ ] Métricas RED por endpoint?
- [ ] Alertas configurados para error rate e latency?
- [ ] Tracing propagado entre serviços?
- [ ] TraceId presente nos logs?
- [ ] Dashboards criados para os métricas principais?
