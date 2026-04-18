---
name: runbook
description: Criação de runbook operacional para incidentes e operação.
---

# Skill: runbook

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
$ARGUMENTS


## Critérios de qualidade
- Evidências explícitas (arquivos, símbolos, comandos, testes).
- Riscos classificados por severidade.
- Escopo controlado e sem refatoração lateral não solicitada.

## Regras de proteção
- Preferir menor mudança defensável.
- Não inferir versões por memória quando houver dependências.
- Não omitir limitações de validação.

