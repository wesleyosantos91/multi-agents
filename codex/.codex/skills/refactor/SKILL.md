---
name: refactor
description: Refatoração segura preservando comportamento externo.
---

# Skill: refactor

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


## Critérios de qualidade
- Evidências explícitas (arquivos, símbolos, comandos, testes).
- Riscos classificados por severidade.
- Escopo controlado e sem refatoração lateral não solicitada.

## Regras de proteção
- Preferir menor mudança defensável.
- Não inferir versões por memória quando houver dependências.
- Não omitir limitações de validação.

