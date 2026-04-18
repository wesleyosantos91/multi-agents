---
name: optimize
description: Análise e otimização de gargalos com validação.
---

# Skill: optimize

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
Analise e otimize a performance do código especificado.

## Processo obrigatório

### 1. Profiling conceitual
- Leia o código-alvo completamente
- Identifique hotspots: loops aninhados, queries N+1, alocações desnecessárias, I/O síncrono bloqueante
- Identifique o gargalo principal (não otimize tudo — otimize o que importa)

### 2. Análise
Acione o `performance-reliability-reviewer` quando a análise exigir profundidade:
- Throughput: o código aguenta a carga esperada?
- Latência: há operações desnecessariamente lentas?
- Concorrência: há contenção, race conditions, locks excessivos?
- Memória: há vazamentos, alocações excessivas, caching ausente?

### 3. Otimização
- Aplique a otimização mais impactante com menor risco
- Prefira mudanças algorítmicas a micro-otimizações
- Documente o trade-off (ex: "usa mais memória para reduzir latência")

### 4. Validação
- Rode os testes existentes — a otimização não pode quebrar comportamento
- Se possível, meça antes/depois (benchmark simples)

### 5. Output
- **Gargalo identificado**: o que era lento e por quê
- **Otimização aplicada**: o que mudou
- **Trade-off**: o que foi sacrificado (se algo)
- **Resultado**: melhoria esperada ou medida

## Agentes disponíveis
- Para análise de performance: acione `performance-reliability-reviewer`
- Para implementar a otimização: use `software-engineer`
- Para validar que não quebrou: use `qa-quality-engineer`

## O que otimizar
$ARGUMENTS


## Critérios de qualidade
- Evidências explícitas (arquivos, símbolos, comandos, testes).
- Riscos classificados por severidade.
- Escopo controlado e sem refatoração lateral não solicitada.

## Regras de proteção
- Preferir menor mudança defensável.
- Não inferir versões por memória quando houver dependências.
- Não omitir limitações de validação.

