---
applyTo: "**/message/**,**/*kafka*/**,**/*sqs*/**,**/*queue*/**,**/*.avsc,**/*asyncapi*.yml,**/*asyncapi*.yaml"
---
# Messaging Instructions

- Trate `message/` como borda assincrona orientada a eventos, nunca request/response.
- Em `message/`, padronize pacotes por responsabilidade (`consumer/`, `producer/`, `event/`, `header/`, `exception/`).
- Nao introduza `request/`, `response/`, `model/` ou `mapper/` dentro de `message/`.
- Exija idempotencia, deduplicacao, retry com backoff/jitter, DLQ e tratamento de poison message.
- Garanta observabilidade de eventos (correlation id, metricas de lag/erro, tracing propagado).
- Evolucao de contratos assincronos deve manter compatibilidade e rollback viavel.

## Referencias

- `docs/ai/roles/architect-reviewer.md`
- `docs/ai/roles/api-contract-reviewer.md`
- `docs/ai/roles/sre-platform-engineer.md`
- `docs/ai/roles/performance-reliability-reviewer.md`
