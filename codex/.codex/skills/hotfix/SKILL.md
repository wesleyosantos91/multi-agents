---
name: hotfix
description: Aplicação de correção emergencial de blast radius mínimo.
---

# Skill: hotfix

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
$ARGUMENTS


## Critérios de qualidade
- Evidências explícitas (arquivos, símbolos, comandos, testes).
- Riscos classificados por severidade.
- Escopo controlado e sem refatoração lateral não solicitada.

## Regras de proteção
- Preferir menor mudança defensável.
- Não inferir versões por memória quando houver dependências.
- Não omitir limitações de validação.

