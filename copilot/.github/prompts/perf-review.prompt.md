---
description: "Prompt reutilizavel do fluxo perf-review para Copilot Chat."
---

Acione o `performance-reliability-reviewer` para análise de performance e confiabilidade.

## Escopo
- Se `{{ARGUMENTS}}` estiver vazio, analise o projeto/branch atual
- Se `{{ARGUMENTS}}` contiver um módulo ou componente, foque nele

## O que avaliar
- Gargalos potenciais (pool sizing, locks, serialização, N+1)
- Riscos de escalabilidade
- Confiabilidade sob carga
- Cold start Lambda (quando aplicável)
- DynamoDB hot partitions (quando aplicável)
- GIL Python, goroutine leaks Go, GC pressure Java (conforme stack)
- SLIs/SLOs e burn rate quando definidos

## Entrada do usuário
{{ARGUMENTS}}

