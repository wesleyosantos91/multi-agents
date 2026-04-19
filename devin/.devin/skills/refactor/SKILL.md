---
name: refactor
description: "Analise e execute o refactoring descrito abaixo com segurança."
argument-hint: "[contexto adicional]"
---

Analise e execute o refactoring descrito abaixo com segurança.

## Processo obrigatório

### 1. Análise prévia
- Leia todo o código afetado antes de qualquer mudança
- Mapeie dependentes: quem usa o código que será refatorado? (Grep por imports, chamadas, referências)
- Identifique testes existentes que cobrem o código

### 2. Planejamento
- Descreva a mudança proposta e o benefício concreto
- Liste os arquivos que serão alterados
- Identifique riscos de regressão

### 3. Execução
- Aplique a mudança preservando comportamento externo
- Respeite o idiomatismo da linguagem e framework
- Não mude o que não precisa mudar

### 4. Validação
- Rode todos os testes do módulo afetado
- Confirme que nenhum dependente quebrou
- Se o refactoring mudou interface pública, atualize os consumidores

### 5. Output
Entregue:
- **O que mudou**: lista de arquivos e natureza da mudança
- **Por que mudou**: benefício concreto
- **Testes**: resultado da validação
- **Breaking changes**: sim/não — se sim, quais e quem é afetado

## Agentes disponíveis (quando necessário)
- Para avaliar impacto arquitetural: acione `architect-reviewer`
- Para avaliar pragmatismo: acione `tech-lead-reviewer`
- Para a execução: use `software-engineer`
- Para validar testes: use `qa-quality-engineer`

## Refactoring solicitado
$ARGUMENTS
