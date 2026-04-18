---
name: pre-pr
description: Checklist técnico final antes de abrir PR.
---

# Skill: pre-pr

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
Execute um checklist completo antes de abrir PR. Acione o `staff-engineer-orchestrator` com os seguintes passos:

## 1. Diff Analysis
- `git diff main...HEAD` para entender todas as mudanças
- Liste arquivos alterados, adicionados e removidos

## 2. Checklist por domínio (acione agentes conforme necessário)
- **tech-lead-reviewer**: pragmatismo, simplicidade, manutenibilidade
- **security-reviewer**: segredos, OWASP, hardening
- **qa-quality-engineer**: cobertura de testes, edge cases, regressões
- **api-contract-reviewer**: breaking changes (se houver mudança de contrato)
- **dependency-versions-reviewer**: versões GA atualizadas (se houver dependências novas/alteradas)

## 3. Validações automáticas
- Verifique se os testes passam (mvn test, go test, pytest, npm test — conforme stack)
- Verifique se há arquivos com segredos (.env, credentials, tokens)
- Verifique se há TODOs/FIXMEs pendentes nas mudanças

## 4. Output
Entregue um relatório estruturado: GO / NO-GO com justificativa por item.

## Contexto adicional
$ARGUMENTS


## Critérios de qualidade
- Evidências explícitas (arquivos, símbolos, comandos, testes).
- Riscos classificados por severidade.
- Escopo controlado e sem refatoração lateral não solicitada.

## Regras de proteção
- Preferir menor mudança defensável.
- Não inferir versões por memória quando houver dependências.
- Não omitir limitações de validação.

