---
description: "Prompt reutilizavel do fluxo runbook para Copilot Chat."
---

Acione o `incident-response-reviewer` e `sre-platform-engineer` para criar um runbook operacional.

## Processo

### 1. Análise do componente
- Leia o código do componente/serviço
- Identifique dependências externas (bancos, filas, APIs, serviços AWS)
- Identifique pontos de falha e modos de degradação

### 2. Estrutura do runbook
Gere o runbook com estas seções:

```markdown
# Runbook: [Nome do Componente]

## Visão geral
O que este componente faz e por que é crítico.

## Dependências
Lista de dependências e impacto se indisponíveis.

## Health checks
Como verificar se o componente está saudável.

## Alarmes
| Alarme | Condição | Severidade | Ação |
|--------|---------|-----------|------|

## Procedimentos de resposta
### [Cenário de falha 1]
1. Diagnóstico: como confirmar o problema
2. Mitigação: ação imediata para restaurar serviço
3. Correção: resolução definitiva
4. Validação: como confirmar que resolveu

## Rollback
Como reverter o último deploy.

## Escalação
Quem contatar e quando.

## Contatos
| Papel | Contato |
|-------|---------|
```

## Componente
{{ARGUMENTS}}

