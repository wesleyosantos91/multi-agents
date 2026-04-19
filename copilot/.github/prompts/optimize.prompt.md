---
description: "Prompt reutilizavel do fluxo optimize para Copilot Chat."
---

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
{{ARGUMENTS}}

