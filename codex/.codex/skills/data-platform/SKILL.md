---
name: data-platform
description: Revisão/desenho de plataforma de dados AWS.
---

# Skill: data-platform

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
Acione o `data-engineering-aws-architect` para análise ou design de plataforma de dados.

## Quando usar
- Pipelines de dados (ETL/ELT)
- Data lake, lakehouse
- Streaming vs batch
- Decisão entre Glue, EMR Serverless, EMR on EC2, Lambda, Step Functions
- Kinesis, MSK, Athena, Redshift, Lake Formation

## Escopo
- Se `$ARGUMENTS` contiver um cenário de dados, analise e recomende arquitetura
- Se `$ARGUMENTS` contiver código de pipeline, revise e otimize

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

