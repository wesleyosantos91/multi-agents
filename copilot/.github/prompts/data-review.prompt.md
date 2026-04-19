---
description: "Prompt reutilizavel do fluxo data-review para Copilot Chat."
---

Acione o `ad-dba-reviewer` para análise de dados e persistência.

## Escopo
- Se `{{ARGUMENTS}}` estiver vazio, analise todas as camadas de dados do projeto
- Se `{{ARGUMENTS}}` contiver uma tabela, query ou decisão de banco, foque nele

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
{{ARGUMENTS}}

