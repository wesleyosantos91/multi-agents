---
applyTo: "**/src/main/**,**/src/test/**,**/*.tf,**/Dockerfile,**/docker-compose*.yml,**/application*.yml,**/application*.yaml,**/application*.properties"
---
# Security Instructions

- Nunca hardcode segredos em codigo, configuracao ou IaC.
- Garanta autenticacao/autorizacao consistente em todas as bordas (`web/` e `message/`).
- Validar entradas e proteger contra injection em APIs, eventos e consultas.
- Nao vazar dados sensiveis em logs, excecoes ou respostas.
- Aplicar hardening de runtime e deploy (Docker, Terraform, AWS).
- Em GraphQL, restringir introspection em producao e controlar complexidade.

## Referencias

- `docs/ai/roles/security-reviewer.md`
- `docs/ai/roles/sre-platform-engineer.md`
- `docs/ai/roles/api-contract-reviewer.md`
