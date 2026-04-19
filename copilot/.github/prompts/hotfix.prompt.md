---
description: "Prompt reutilizavel do fluxo hotfix para Copilot Chat."
---

Aplique uma correção emergencial com blast radius mínimo.

## Regras de hotfix
- **Menor mudança possível** — corrija o problema e nada mais
- **Sem refatoração** — não é o momento
- **Sem features** — não aproveite para adicionar funcionalidade
- **Teste obrigatório** — a correção deve ser validada

## Processo obrigatório

### 1. Entendimento
- Leia o código envolvido no problema
- Identifique a causa raiz com precisão
- Confirme que a correção proposta não introduz efeitos colaterais

### 2. Correção
- Aplique a menor mudança que resolve o problema
- Documente no código com comentário breve SE a correção não for óbvia

### 3. Validação
- Rode os testes do módulo afetado
- Crie um teste mínimo que cobre o cenário do bug (se não existir)
- Confirme que nenhum teste existente quebrou

### 4. Output
Entregue:
- **Causa raiz**: uma frase
- **Correção**: o que mudou (arquivos e linhas)
- **Blast radius**: quais outros componentes poderiam ser afetados
- **Testes**: resultado
- **Rollback**: como reverter se necessário (git revert do commit)

## Agentes
- Para a correção: use `software-engineer`
- Para validar segurança (se relevante): acione `security-reviewer`
- Para validar testes: use `qa-quality-engineer`

## Problema
{{ARGUMENTS}}

