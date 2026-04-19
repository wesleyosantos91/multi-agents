---
name: migrate
description: Planejamento e execução segura de migração técnica.
---

# Skill: migrate

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


## Critérios de qualidade
- Evidências explícitas (arquivos, símbolos, comandos, testes).
- Riscos classificados por severidade.
- Escopo controlado e sem refatoração lateral não solicitada.

## Regras de proteção
- Preferir menor mudança defensável.
- Não inferir versões por memória quando houver dependências.
- Não omitir limitações de validação.

