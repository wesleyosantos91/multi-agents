---
name: adr
description: "Acione o `tech-writer` para criar um novo Architecture Decision Record (ADR)."
argument-hint: "[contexto adicional]"
---

Acione o `tech-writer` para criar um novo Architecture Decision Record (ADR).

## Local
- Salve em `docs/architecture/adr/`
- Use numeração sequencial (verifique o último ADR existente)

## Formato
Use o template padrão:
```
# ADR-NNNN: Título da Decisão

## Status
Proposta | Aceita | Depreciada | Substituída por ADR-XXXX

## Contexto
O que motiva esta decisão? Qual problema estamos resolvendo?

## Decisão
O que decidimos fazer e por quê.

## Consequências
### Positivas
### Negativas
### Riscos

## Alternativas Consideradas
Opção A / Opção B — por que foram descartadas.
```

## Decisão a documentar
$ARGUMENTS
