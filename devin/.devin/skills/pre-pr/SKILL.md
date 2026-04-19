---
name: pre-pr
description: "Execute um checklist completo antes de abrir PR. Acione o `staff-engineer-orchestrator` com os seguintes passos:"
argument-hint: "[contexto adicional]"
---

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
