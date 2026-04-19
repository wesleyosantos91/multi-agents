---
name: aws-lambda-checklist
description: Skill importada do EXEMPLO (aws-lambda-checklist.md).
allowed-tools: "read,search"
user-invocable: true
---

# Skill

---
name: aws-lambda-checklist
description: "Checklist completo para Lambda AWS: handler, IAM, observabilidade, deploy e operação. Use quando criar, revisar ou deployar Lambda functions."
---

# AWS Lambda — Production Checklist

Checklist completo para Lambda em produção.

## Handler

### Estrutura
```
handler(event, context)
  → validate input
  → call business logic (testável sem AWS SDK)
  → return response
```

- Handler é fino — apenas entrada/saída
- Lógica de negócio separada e testável isoladamente
- Nunca processar lógica complexa diretamente no handler

### Cold start
- Inicializar SDK clients e conexões FORA do handler (module-level)
- Java: usar Quarkus/Micronaut (startup rápido) ou SnapStart
- Python: import lazy para módulos pesados
- Go: naturalmente rápido — atenção ao tamanho do binário

## IAM — Menor privilégio

```hcl
# ERRADO
resource "aws_iam_policy" "bad" {
  policy = jsonencode({
    Statement = [{
      Effect   = "Allow"
      Action   = "*"
      Resource = "*"
    }]
  })
}

# CORRETO
resource "aws_iam_policy" "good" {
  policy = jsonencode({
    Statement = [{
      Effect   = "Allow"
      Action   = ["dynamodb:GetItem", "dynamodb:PutItem"]
      Resource = "arn:aws:dynamodb:*:*:table/orders"
    }]
  })
}
```

## Configuração

| Config | Recomendação |
|--------|-------------|
| Timeout | 3-5x o p99 observado — nunca deixar default (3s) ou máximo (900s) |
| Memory | Testar com AWS Lambda Power Tuning — mais memória = mais CPU |
| Reserved concurrency | Definir para proteger downstream |
| Environment vars | Configuração sim, segredos NÃO — usar Secrets Manager |

## Observabilidade

- **Logs**: JSON estruturado com requestId, traceId
- **Métricas**: Duration, Errors, Throttles, ConcurrentExecutions
- **Tracing**: X-Ray ou ADOT habilitado
- **Alarmes**: Errors > 0, Throttles > 0, Duration > 80% do timeout

## Deploy

- **Versions e aliases**: nunca deployar direto em `$LATEST`
- **Alias `prod`**: apontar para version específica
- **Canary/Blue-Green**: CodeDeploy com alarmes de rollback
- **Event source mapping**: apontar para alias, não `$LATEST`

## Error handling

### SQS → Lambda
- Configurar `maxReceiveCount` no SQS
- DLQ para mensagens que falham
- `ReportBatchItemFailures` para partial batch failure
- Idempotência: mesmo evento 2x deve dar mesmo resultado

### API Gateway → Lambda
- Resposta de erro padronizada (RFC 9457)
- Timeout do API Gateway < timeout da Lambda
- Throttling configurado no API Gateway

## Checklist final
- [ ] Handler fino, lógica testável separadamente?
- [ ] IAM com menor privilégio (sem `*`)?
- [ ] Timeout adequado (não default, não máximo)?
- [ ] Memory dimensionada?
- [ ] Reserved concurrency definida?
- [ ] Segredos via Secrets Manager (não env vars)?
- [ ] Logs estruturados JSON?
- [ ] Alarmes: Errors, Throttles, Duration?
- [ ] X-Ray/ADOT habilitado?
- [ ] Deploy via versions + aliases?
- [ ] Canary ou blue/green configurado?
- [ ] DLQ configurada?
- [ ] Idempotência implementada?
- [ ] Testes com payloads válidos e malformados?
