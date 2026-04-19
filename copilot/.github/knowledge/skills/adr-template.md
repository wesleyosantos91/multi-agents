---
name: adr-template
description: "Template e guia para ADRs (Architecture Decision Records): quando criar, estrutura, exemplos. Use quando documentar decisões arquiteturais ou criar ADRs."
---

# ADR — Architecture Decision Records

Guia para documentar decisoes arquiteturais significativas.

## Quando criar um ADR

- Escolha de tecnologia (banco, fila, linguagem, framework)
- Mudanca de padrao arquitetural (monolito → microservicos)
- Decisao de trade-off significativa (consistencia vs disponibilidade)
- Mudanca de estrategia (deploy, error handling, autenticacao)
- Quando alguem perguntaria "por que fizemos assim?"

**NAO criar ADR para**: escolha de nome de variavel, formatacao de codigo, decisoes triviais e reversiveis.

## Template

```markdown
# ADR-NNNN: Titulo curto e descritivo

**Status**: Proposed | Accepted | Deprecated | Superseded by ADR-XXXX
**Date**: YYYY-MM-DD
**Deciders**: Quem participou da decisao
**Technical Story**: Link para issue/ticket (se houver)

## Context

Qual e o contexto e o problema que motivou essa decisao?
Quais forcas estao em jogo (tecnicas, organizacionais, de negocio)?
Qual e a situacao atual e por que ela nao e mais adequada?

## Decision

Qual e a decisao tomada e por que?
Descreva a abordagem escolhida de forma clara e objetiva.

## Alternatives Considered

### Alternativa 1: Nome
- **Descricao**: O que seria feito
- **Pros**: Vantagens
- **Cons**: Desvantagens
- **Por que descartada**: Motivo principal

### Alternativa 2: Nome
- **Descricao**: O que seria feito
- **Pros**: Vantagens
- **Cons**: Desvantagens
- **Por que descartada**: Motivo principal

## Consequences

### Positivas
- Beneficio 1
- Beneficio 2

### Negativas
- Trade-off 1
- Trade-off 2

### Riscos
- Risco identificado e mitigacao planejada

## Compliance

- [ ] Revisado pelo time
- [ ] Alinhado com arquitetura existente
- [ ] Impacto em seguranca avaliado
- [ ] Impacto em custo avaliado
```

## Exemplos

### ADR-0001: DynamoDB para persistencia de pedidos

```markdown
# ADR-0001: DynamoDB para persistencia de pedidos

**Status**: Accepted
**Date**: 2026-03-15
**Deciders**: Time de engenharia

## Context

O servico de pedidos precisa de um banco de dados para armazenar pedidos.
O padrao de acesso e predominantemente key-value (busca por ID) com queries
secundarias por status e data. O volume esperado e 10K pedidos/dia,
com picos de ate 100 pedidos/segundo.

O servico roda como Lambda na AWS, o que favorece servicos gerenciados
sem connection pooling.

## Decision

Usar DynamoDB com:
- Partition key: `orderId` (UUID)
- GSI1: `status-createdAt-index` para queries por status com ordenacao
- On-demand capacity (pay-per-request)
- Point-in-time recovery habilitado

## Alternatives Considered

### PostgreSQL (RDS)
- **Pros**: Modelo relacional flexivel, SQL, joins
- **Cons**: Connection pooling necessario com Lambda, custo fixo (instancia),
  gerenciamento de schema mais complexo
- **Descartada**: O padrao de acesso nao justifica complexidade relacional.
  Lambda + RDS precisa de RDS Proxy ($), e o volume nao justifica instancia fixa.

### Aurora Serverless v2
- **Pros**: Serverless, SQL, auto-scaling
- **Cons**: Custo minimo maior que DynamoDB on-demand, cold start no scale-up,
  connection pooling ainda necessario
- **Descartada**: Custo minimo desproporcional ao volume esperado.

## Consequences

### Positivas
- Zero management (fully managed)
- Custo proporcional ao uso (on-demand)
- Latencia single-digit ms para acesso por key
- Integracao nativa com Lambda (SDK, sem driver)

### Negativas
- Queries complexas limitadas (sem joins, sem aggregations)
- Modelagem de dados requer planejamento upfront (access patterns)
- GSIs adicionam custo e complexidade

### Riscos
- Se surgirem queries complexas nao previstas, pode ser necessario
  adicionar mais GSIs ou considerar um servico de query separado (Athena/OpenSearch).
```

### ADR-0002: SQS + Lambda para processamento assincrono

```markdown
# ADR-0002: SQS + Lambda para processamento assincrono

**Status**: Accepted
**Date**: 2026-03-15
**Deciders**: Time de engenharia

## Context

Apos criacao de um pedido, e necessario:
1. Processar pagamento
2. Enviar notificacao
3. Atualizar metricas

Essas operacoes nao devem bloquear a resposta ao usuario.
Precisamos de processamento assincrono confiavel com retry e DLQ.

## Decision

SQS Standard Queue com Lambda trigger:
- BatchSize: 10
- ReportBatchItemFailures: habilitado (partial batch failure)
- DLQ com maxReceiveCount: 3
- VisibilityTimeout: 300s (5x Lambda timeout de 60s)

## Alternatives Considered

### EventBridge + Lambda
- **Pros**: Fan-out nativo, event routing por regras
- **Cons**: Sem batching nativo, retry mais limitado, sem FIFO
- **Descartada**: SQS oferece controle mais fino de retry e DLQ
  para processamento transacional.

### Step Functions
- **Pros**: Orquestracao visual, retry por step, error handling granular
- **Cons**: Custo por transicao de estado, overhead para fluxo simples
- **Descartada**: Overengineering para 3 steps sem branching complexo.

## Consequences

### Positivas
- Desacoplamento total entre API e processamento
- Retry automatico com backoff
- DLQ para mensagens que falharam (investigacao e reprocessamento)
- Partial batch failure evita reprocessamento desnecessario

### Negativas
- At-least-once delivery — consumer DEVE ser idempotente
- Sem ordering garantido (Standard Queue)
- Latencia adicional (ms a segundos) entre producao e consumo
```

## Naming e organizacao

```
.github/knowledge/docs-reference/architecture/adr/
├── 0001-dynamodb-for-orders.md
├── 0002-sqs-lambda-async-processing.md
├── 0003-report-batch-item-failures.md
├── 0004-floci-local-emulator.md
└── README.md  # indice com status de cada ADR
```

### Indice (README.md)

```markdown
# Architecture Decision Records

| ADR | Titulo | Status | Data |
|-----|--------|--------|------|
| 0001 | DynamoDB para pedidos | Accepted | 2026-03-15 |
| 0002 | SQS+Lambda async | Accepted | 2026-03-15 |
| 0003 | ReportBatchItemFailures | Accepted | 2026-03-20 |
| 0004 | Floci como emulador | Accepted | 2026-04-01 |
```

## Boas praticas

- **Imutabilidade**: ADRs aceitos nao sao editados. Se a decisao muda, crie um novo ADR e marque o antigo como `Superseded by ADR-XXXX`
- **Concisao**: 1-2 paginas maximo. Se precisar de mais, o escopo esta amplo demais
- **Alternativas reais**: listar apenas opcoes que foram realmente consideradas
- **Consequencias honestas**: listar trade-offs negativos — isso agrega valor
- **Revisao**: ADRs devem ser revisados pelo time antes de aceitos

## Checklist

- [ ] Titulo descreve a decisao (nao o problema)?
- [ ] Contexto explica o "por que agora"?
- [ ] Decisao e clara e objetiva?
- [ ] Alternativas foram realmente consideradas (nao strawman)?
- [ ] Consequencias incluem trade-offs negativos?
- [ ] Status esta correto (Proposed → Accepted)?
- [ ] Numeracao sequencial sem gaps?
- [ ] Indice atualizado?

