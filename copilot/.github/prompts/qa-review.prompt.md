---
description: "Prompt reutilizavel do fluxo qa-review para Copilot Chat."
---

Acione o `qa-quality-engineer` para análise de qualidade e cobertura de testes.

## Escopo
- Se `{{ARGUMENTS}}` estiver vazio, analise o projeto/branch atual
- Se `{{ARGUMENTS}}` contiver um módulo, foque nele

## O que avaliar
- Cobertura de testes (unitários, integração, contrato, e2e)
- Edge cases não cobertos
- Testes de comportamento em falha
- Regressões potenciais
- Testes faltantes com justificativa de risco
- Ferramentas por linguagem: JUnit 5/PIT/ArchUnit/Testcontainers (Java), pytest (Python), testing/-race (Go), Jest/Playwright (Frontend)

## Entrada do usuário
{{ARGUMENTS}}

