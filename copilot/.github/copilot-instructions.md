# Copilot Instructions - Multi-Agent Configuration

## Escopo

Esta configuracao opera somente via `.github`:

- `.github/agents/*.agent.md`
- `.github/instructions/*.instructions.md`
- `.github/prompts/*.prompt.md`
- `.github/skills/*/SKILL.md`
- `.github/hooks/*.json`
- `.github/copilot/settings*.json`
- `.github/knowledge/*`

## Regra principal

- Demandas nao triviais devem iniciar em `staff-engineer-orchestrator`.
- Nao implementar antes de consolidar analise dos especialistas relevantes.

## Sistema critico

Sempre considerar: resiliencia, seguranca, observabilidade, operabilidade e risco de producao.

## Dependencias

Nunca assumir versoes por memoria. Acione `dependency-versions-reviewer` quando houver mudanca de dependencias.
