---
name: debug
description: Diagnóstico de causa raiz e correção mínima segura.
---

# Skill: debug

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
Investigue e resolva o problema descrito abaixo usando análise de causa raiz sistemática.

## Processo obrigatório

### 1. Reprodução
- Leia o código envolvido e entenda o fluxo
- Identifique o ponto exato onde o comportamento diverge do esperado
- Se possível, rode testes ou comandos que reproduzam o problema

### 2. Diagnóstico
- Trace o fluxo de dados do input ao output
- Identifique hipóteses de causa raiz (liste pelo menos 2)
- Valide cada hipótese com evidência do código — não assuma

### 3. Correção
- Aplique a menor correção que resolve a causa raiz
- Não refatore código adjacente que não faz parte do problema
- Garanta que a correção não introduz regressão

### 4. Validação
- Rode os testes existentes para confirmar que nada quebrou
- Se não há teste que cobre o cenário, crie um teste mínimo

### 5. Output
Entregue:
- **Causa raiz**: uma frase
- **Correção aplicada**: o que mudou e por quê
- **Testes**: quais passaram, qual foi criado (se aplicável)
- **Risco residual**: algo que deve ser monitorado

## Agentes disponíveis (quando necessário)
- Se o bug envolver segurança: acione `security-reviewer`
- Se o bug envolver performance: acione `performance-reliability-reviewer`
- Para a correção: use `software-engineer`
- Para validar testes: use `qa-quality-engineer`

## Problema
$ARGUMENTS


## Critérios de qualidade
- Evidências explícitas (arquivos, símbolos, comandos, testes).
- Riscos classificados por severidade.
- Escopo controlado e sem refatoração lateral não solicitada.

## Regras de proteção
- Preferir menor mudança defensável.
- Não inferir versões por memória quando houver dependências.
- Não omitir limitações de validação.

