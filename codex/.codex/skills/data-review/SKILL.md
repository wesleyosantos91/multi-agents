---
name: data-review
description: Revisão de modelagem/persistência transacional e queries.
---

# Skill: data-review

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
Acione o `ad-dba-reviewer` para análise de dados e persistência.

## Escopo
- Se `$ARGUMENTS` estiver vazio, analise todas as camadas de dados do projeto
- Se `$ARGUMENTS` contiver uma tabela, query ou decisão de banco, foque nele

## O que avaliar
- Escolha de banco (DynamoDB vs RDS/Aurora) justificada
- Modelagem de dados e access patterns
- Índices (GSI/LSI para DynamoDB, índices para RDS)
- Queries otimizadas (sem N+1, sem full scan)
- Idempotência (ConditionExpression para DynamoDB)
- Hot partition prevention
- Connection pooling e timeout
- Backup, PITR, KMS encryption
- Lambda + DynamoDB: cliente fora do handler
- Lambda + RDS: RDS Proxy configurado

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

