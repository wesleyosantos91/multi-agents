---
name: perf-review
description: Revisão de performance e confiabilidade sob carga.
---

# Skill: perf-review

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
Acione o `performance-reliability-reviewer` para análise de performance e confiabilidade.

## Escopo
- Se `$ARGUMENTS` estiver vazio, analise o projeto/branch atual
- Se `$ARGUMENTS` contiver um módulo ou componente, foque nele

## O que avaliar
- Gargalos potenciais (pool sizing, locks, serialização, N+1)
- Riscos de escalabilidade
- Confiabilidade sob carga
- Cold start Lambda (quando aplicável)
- DynamoDB hot partitions (quando aplicável)
- GIL Python, goroutine leaks Go, GC pressure Java (conforme stack)
- SLIs/SLOs e burn rate quando definidos

## Entrada do usuário
$ARGUMENTS


## Critérios de qualidade
- Evidências explícitas (arquivos, símbolos, comandos, testes).
- Riscos classificados por severidade.
- Escopo controlado e sem refatoração lateral não solicitada.

## Regras de proteção
- Preferir menor mudança defensável.
- Não inferir versões por memória quando houver dependências.
- Não omitir limitações de validação.

