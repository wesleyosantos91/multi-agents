---
name: review
description: Revisão técnica completa de mudanças com consolidação multiagente.
---

# Skill: review

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


## Critérios de qualidade
- Evidências explícitas (arquivos, símbolos, comandos, testes).
- Riscos classificados por severidade.
- Escopo controlado e sem refatoração lateral não solicitada.

## Regras de proteção
- Preferir menor mudança defensável.
- Não inferir versões por memória quando houver dependências.
- Não omitir limitações de validação.

