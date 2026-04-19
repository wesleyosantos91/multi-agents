---
name: quick-fix
description: "Aplique uma correção rápida e pontual SEM acionar o orquestrador completo."
argument-hint: "[contexto adicional]"
---

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
