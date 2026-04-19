---
name: migrate
description: "Planeje e execute uma migração técnica com segurança."
argument-hint: "[contexto adicional]"
---

Planeje e execute uma migração técnica com segurança.

## Processo obrigatório

### 1. Inventário
- Mapeie todo código afetado pela migração (Glob + Grep)
- Liste dependências, consumidores e integrações impactadas
- Identifique testes existentes que cobrem o código afetado

### 2. Análise de risco
Acione o `staff-engineer-orchestrator` para avaliar:
- **architect-reviewer**: impacto arquitetural da migração
- **api-contract-reviewer**: breaking changes em contratos (se aplicável)
- **security-reviewer**: novos riscos de segurança (se mudar autenticação, dependências, etc.)
- **dependency-versions-reviewer**: versões corretas dos novos componentes

### 3. Plano de migração
Entregue um plano com:
- **Etapas ordenadas**: cada passo da migração
- **Compatibilidade**: como manter backward compatibility durante a transição (se necessário)
- **Rollback**: como reverter cada etapa se algo falhar
- **Testes**: como validar cada etapa

### 4. Execução (se aprovado)
- Execute etapa por etapa
- Valide testes após cada etapa
- Pare e reporte se algo inesperado acontecer

## O que migrar
$ARGUMENTS
