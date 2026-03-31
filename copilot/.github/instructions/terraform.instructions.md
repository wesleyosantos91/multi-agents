---
applyTo: "**/*.tf,**/*.tfvars,**/.terraform.lock.hcl"
---
# Terraform Instructions

- Organize modulos, variaveis e outputs com naming consistente por ambiente.
- Nao hardcode segredos; use mecanismos seguros de injecao/gestao de credenciais.
- Priorize mudancas incrementais e rollback previsivel para reduzir risco de producao.
- Explicite impactos de state, dependencias e ordem de aplicacao.
- Alinhe recursos e politicas com padroes AWS e requisitos de operacao do sistema critico.

## Referencias

- `docs/ai/roles/sre-platform-engineer.md`
- `docs/ai/roles/security-reviewer.md`
- `docs/ai/orchestration/staff-engineer-orchestrator.md`
