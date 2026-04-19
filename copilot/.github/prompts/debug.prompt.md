---
description: "Prompt reutilizavel do fluxo debug para Copilot Chat."
---

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
{{ARGUMENTS}}

