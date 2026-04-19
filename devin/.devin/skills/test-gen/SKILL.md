---
name: test-gen
description: "Gere ou melhore testes para o código especificado."
argument-hint: "[contexto adicional]"
---

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
