---
applyTo: "**/web/**,**/*.proto,**/*openapi*/**,**/*graphql*/**,**/*schema.graphql,**/*schema.gql"
---
# API Instructions

- Trate `web/` como borda sincrona, com separacao clara entre REST, gRPC e GraphQL.
- Nao exponha entidades de dominio diretamente em contratos de borda.
- Use contratos formais e versionados (OpenAPI, Protobuf, GraphQL Schema) com compatibilidade evolutiva.
- Breaking changes devem ser explicitas, justificadas e acompanhadas de estrategia de migracao.
- Padronize erro por protocolo; em REST, prefira Problem Details (RFC 9457) quando aplicavel.
- Em GraphQL, controle profundidade/complexidade e mitigue N+1 quando necessario.

## Referencias

- `docs/ai/roles/api-contract-reviewer.md`
- `docs/ai/roles/architect-reviewer.md`
- `docs/ai/roles/security-reviewer.md`
