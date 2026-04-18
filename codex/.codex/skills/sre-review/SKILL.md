---
name: sre-review
description: Revisão de operabilidade, observabilidade e readiness.
---

# Skill: sre-review

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
Acione o `sre-platform-engineer` para análise de operabilidade e plataforma.

## Escopo
- Se `$ARGUMENTS` estiver vazio, analise o projeto/branch atual
- Se `$ARGUMENTS` contiver um módulo ou aspecto operacional, foque nele

## O que avaliar
- Deployability e rollback
- Readiness/liveness probes
- Logs estruturados (JSON)
- Métricas e tracing distribuído
- Terraform: organização, state, naming
- Docker e ambiente local
- Lambda versions/aliases, deploy strategy
- CloudWatch Alarms configurados
- Ministack cobrindo serviços AWS

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

