---
applyTo: "**/.github/workflows/*.yml,**/.github/workflows/*.yaml,**/Dockerfile,**/docker-compose*.yml,**/docker-compose*.yaml"
---
# CI/CD Instructions

- Pipeline deve ter gates minimos: lint, testes, build e seguranca.
- Planejar estrategia de deploy com rollback claro (blue/green ou canary quando aplicavel).
- Evitar credenciais estaticas em CI; priorizar OIDC e segredos gerenciados.
- Publicacao para producao deve ser rastreavel e com criterio explicito de promocao.

## Referencia
- `.github/knowledge/agents/cicd-pipeline-engineer.md`
