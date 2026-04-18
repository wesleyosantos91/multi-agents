---
name: incident-readiness
description: Avaliação de prontidão para incidentes em produção.
---

# Skill: incident-readiness

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
Acione o `incident-response-reviewer` para avaliar a prontidão do sistema para incidentes em produção.

## O que verificar
- SLOs/SLIs definidos por componente crítico
- SLIs mapeados para métricas AWS reais
- CloudWatch Alarms configurados para SLO breach
- Runbooks existem para cada alarme crítico
- Template de postmortem definido
- On-call e escalada documentados
- Error budgets definidos
- Chaos engineering (AWS FIS) considerado

## Escopo
- Se `$ARGUMENTS` estiver vazio, avalie o sistema completo
- Se `$ARGUMENTS` contiver um componente, foque nele

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

