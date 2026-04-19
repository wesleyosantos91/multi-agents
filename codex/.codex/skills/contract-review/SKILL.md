---
name: contract-review
description: Revisão de contratos de borda e compatibilidade evolutiva.
---

# Skill: contract-review

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
Acione o `api-contract-reviewer` para análise de contratos de borda.

## Escopo
- Se `$ARGUMENTS` estiver vazio, analise todos os contratos do projeto (OpenAPI, Protobuf, GraphQL, Avro, AsyncAPI)
- Se `$ARGUMENTS` contiver um contrato ou endpoint, foque nele

## O que avaliar
- Breaking changes identificados com severidade
- Backward/forward compatibility
- Schema governance e versionamento
- Naming consistente
- Contract tests existem
- Consumers mobile: período de backward compatibility de 90 dias / 3 releases

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

