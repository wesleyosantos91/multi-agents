---
name: contract-review
description: "Acione o `api-contract-reviewer` para análise de contratos de borda."
argument-hint: "[contexto adicional]"
---

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
