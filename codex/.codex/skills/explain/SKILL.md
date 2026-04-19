---
name: explain
description: Explicação técnica de código, arquitetura e fluxo.
---

# Skill: explain

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
$ARGUMENTS


## Critérios de qualidade
- Evidências explícitas (arquivos, símbolos, comandos, testes).
- Riscos classificados por severidade.
- Escopo controlado e sem refatoração lateral não solicitada.

## Regras de proteção
- Preferir menor mudança defensável.
- Não inferir versões por memória quando houver dependências.
- Não omitir limitações de validação.

