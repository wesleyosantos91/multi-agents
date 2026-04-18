---
name: test-gen
description: Geração e melhoria de testes orientados a comportamento.
---

# Skill: test-gen

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
Gere ou melhore testes para o código especificado.

## Processo obrigatório

### 1. Análise do código
- Leia o código-alvo completamente
- Identifique a linguagem e framework de teste (JUnit 5, pytest, testing/Go, Jest, XCTest)
- Identifique os caminhos: happy path, edge cases, error cases
- Identifique dependências externas que precisam de mock/stub

### 2. Análise de testes existentes
- Leia os testes existentes (se houver)
- Identifique gaps de cobertura
- Não duplique testes que já existem

### 3. Geração de testes
- Gere testes que validam **comportamento**, não implementação
- Cubra: happy path, edge cases, error/exception cases
- Use o estilo e padrões dos testes existentes no projeto
- Use ferramentas idiomáticas:
  - Java: JUnit 5 + Testcontainers quando integração
  - Python: pytest + fixtures + parametrize
  - Go: table-driven tests + t.Run
  - Frontend: Testing Library + MSW
  - Mobile: Compose Test / XCTest

### 4. Validação
- Rode os testes gerados e confirme que passam
- Confirme que testes existentes continuam passando

### 5. Output
Entregue:
- **Testes criados**: lista com descrição de cada cenário
- **Cobertura**: quais caminhos estão cobertos agora
- **Gaps remanescentes**: o que ainda não está coberto e por quê

## Agentes disponíveis (quando necessário)
- Para gerar/melhorar testes: use `qa-quality-engineer`
- Para implementar os testes: use `software-engineer`
- Para avaliar edge cases de segurança: acione `security-reviewer`

## Alvo
$ARGUMENTS


## Critérios de qualidade
- Evidências explícitas (arquivos, símbolos, comandos, testes).
- Riscos classificados por severidade.
- Escopo controlado e sem refatoração lateral não solicitada.

## Regras de proteção
- Preferir menor mudança defensável.
- Não inferir versões por memória quando houver dependências.
- Não omitir limitações de validação.

