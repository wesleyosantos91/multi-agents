---
description: "Prompt reutilizavel do fluxo explain para Copilot Chat."
---

Explique o código, arquitetura ou fluxo especificado de forma clara e objetiva.

## Processo

### 1. Leitura
- Leia o código/arquivos relevantes completamente
- Identifique dependências e integrações
- Trace o fluxo de dados de ponta a ponta

### 2. Explicação
Estruture a explicação em:

- **O que faz**: descrição funcional em 1-3 frases
- **Como funciona**: fluxo passo a passo (entrada → processamento → saída)
- **Por que foi feito assim**: decisões de design observáveis no código
- **Dependências**: o que este código usa e quem usa este código
- **Pontos de atenção**: complexidade, riscos, edge cases observados

### 3. Diagrama (quando aplicável)
Se o fluxo envolver múltiplos componentes, inclua um diagrama textual simples (mermaid ou ASCII).

## Regras
- Baseie-se exclusivamente no código — não invente intenções
- Adapte o nível de detalhe ao que foi pedido
- Se o código é simples, a explicação deve ser curta

## Agentes disponíveis (quando necessário)
- Para explicação de arquitetura: acione `architect-reviewer`
- Para explicação de segurança: acione `security-reviewer`
- Para explicação de dados: acione `ad-dba-reviewer`

## O que explicar
{{ARGUMENTS}}

