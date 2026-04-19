---
name: qa-review
description: Revisão de qualidade e estratégia de testes.
---

# Skill: qa-review

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
Acione o `qa-quality-engineer` para análise de qualidade e cobertura de testes.

## Escopo
- Se `$ARGUMENTS` estiver vazio, analise o projeto/branch atual
- Se `$ARGUMENTS` contiver um módulo, foque nele

## O que avaliar
- Cobertura de testes (unitários, integração, contrato, e2e)
- Edge cases não cobertos
- Testes de comportamento em falha
- Regressões potenciais
- Testes faltantes com justificativa de risco
- Ferramentas por linguagem: JUnit 5/PIT/ArchUnit/Testcontainers (Java), pytest (Python), testing/-race (Go), Jest/Playwright (Frontend)

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

