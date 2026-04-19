---
name: review
description: "Acione o `staff-engineer-orchestrator` para fazer uma revisão completa do código alterado na branch atual."
argument-hint: "[contexto adicional]"
---

Acione o `staff-engineer-orchestrator` para fazer uma revisão completa do código alterado na branch atual.

## Contexto
- Compare com a branch `main` usando `git diff main...HEAD`
- Identifique todos os arquivos alterados
- Classifique o nível da demanda (trivial, pontual, moderado, full)

## O que revisar
- Acione os agentes relevantes conforme a ordem definida no CLAUDE.md
- Consolide achados, resolva conflitos e entregue o plano final estruturado
- Diferencie riscos críticos de melhorias futuras

## Entrada do usuário
$ARGUMENTS
