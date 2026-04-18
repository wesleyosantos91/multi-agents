---
name: quick-fix
description: Correção rápida e pontual de baixo risco.
---

# Skill: quick-fix

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
Aplique uma correção rápida e pontual SEM acionar o orquestrador completo.

## Quando usar
- Mudanças triviais: typo, import faltando, config incorreta, nome errado
- Escopo claro e limitado: 1-3 arquivos
- Sem risco arquitetural

## Quando NÃO usar (use /implement ou /review)
- Mudança afeta múltiplos módulos
- Mudança altera contrato de API
- Mudança envolve segurança ou dados sensíveis

## Processo
1. Leia o código envolvido
2. Aplique a correção mínima
3. Rode os testes do módulo afetado (se existirem)
4. Reporte o que mudou em 1-3 linhas

## Agente
Use `software-engineer` diretamente — sem orquestração.

## Correção
$ARGUMENTS


## Critérios de qualidade
- Evidências explícitas (arquivos, símbolos, comandos, testes).
- Riscos classificados por severidade.
- Escopo controlado e sem refatoração lateral não solicitada.

## Regras de proteção
- Preferir menor mudança defensável.
- Não inferir versões por memória quando houver dependências.
- Não omitir limitações de validação.

