---
description: "Prompt reutilizavel do fluxo review para Copilot Chat."
---

Acione o `staff-engineer-orchestrator` para fazer uma revisão completa do código alterado na branch atual.

## Contexto
- Compare com a branch `main` usando `git diff main...HEAD`
- Identifique todos os arquivos alterados
- Classifique o nível da demanda (trivial, pontual, moderado, full)

## O que revisar
- Acione os agentes relevantes conforme a ordem definida no .github/copilot-instructions.md
- Consolide achados, resolva conflitos e entregue o plano final estruturado
- Diferencie riscos críticos de melhorias futuras

## Entrada do usuário
{{ARGUMENTS}}

