---
name: adr
description: Geração de ADR com contexto, decisão, trade-offs e consequências.
---

# Skill: adr

## Quando dispara
- Quando o usuário solicitar explicitamente o workflow $name.
- Quando o contexto da tarefa for compatível com o objetivo descrito nesta skill.

## Quando NÃO dispara
- Quando a tarefa exigir outro workflow mais específico do catálogo.
- Quando o escopo não tiver relação com o objetivo técnico desta skill.

## Inputs esperados
- Contexto da demanda.
- Escopo ou módulo alvo (quando aplicável).
- Restrições técnicas e de risco.

## Saída esperada
- Diagnóstico objetivo com evidências.
- Recomendação acionável e priorizada.
- Plano de validação proporcional ao risco.

## Workflow passo a passo
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


## Critérios de qualidade
- Evidências explícitas (arquivos, símbolos, comandos, testes).
- Riscos classificados por severidade.
- Escopo controlado e sem refatoração lateral não solicitada.

## Regras de proteção
- Preferir menor mudança defensável.
- Não inferir versões por memória quando houver dependências.
- Não omitir limitações de validação.

