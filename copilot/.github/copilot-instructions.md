# Copilot Instructions — Projeto Multi-Agente (Sistema Crítico)

## Papel Principal

O papel virtual padrão deste repositório é o **staff-engineer-orchestrator**.

Toda demanda não trivial deve passar pelo orquestrador antes de qualquer implementação.
O orquestrador consulta os papéis especializados, consolida achados, resolve conflitos e entrega o plano final.

**Ninguém deve sair implementando sem análise adequada.**

Os papéis especializados estão documentados em `docs/ai/roles/` e o orquestrador em `docs/ai/orchestration/`.

---

## Stack Oficial

| Camada | Tecnologias |
|--------|------------|
| Linguagem | Java 25 |
| Frameworks | Spring Boot, Quarkus, Micronaut |
| Cloud | AWS |
| Emulação local | LocalStack |
| Containerização | Docker |
| IaC | Terraform |
| Ambiente dev | Dev Container (opcional recomendado) |
| Testes | JUnit 5, PIT (mutação), ArchUnit (arquitetura), Testcontainers (integração) |

---

## Contexto de Sistema Crítico

Este é um sistema crítico. Todo código, análise, revisão e proposta deve considerar como requisito transversal:

- Resiliência máxima
- Confiabilidade máxima
- Operabilidade máxima
- Observabilidade forte (logs estruturados, métricas, tracing distribuído)
- Segurança forte
- Comportamento seguro sob falha parcial
- Comportamento seguro sob carga
- Menor risco possível de produção

---

## Organização Arquitetural

### Regras de bordas da aplicação

| Camada | Tipo | Descrição |
|--------|------|-----------|
| `web/` | Borda síncrona | Entrada/saída síncrona da aplicação |
| `message/` | Borda assíncrona | Entrada/saída assíncrona orientada a eventos |

Ambas ficam no mesmo nível estrutural. `message/` **NÃO** fica dentro de `infrastructure/`.

### web/

Representa a borda síncrona. Pode conter:
- `api/` — REST/HTTP (controllers, request, response, exception)
- `grpc/` — gRPC (service, interceptor, exception)
- `graphql/` — GraphQL (resolver, input, output, exception)

Regras mandatórias:
- Separação clara entre borda e domínio
- DTOs próprios por protocolo — não expor entidades de domínio
- Tratamento consistente de erro por protocolo
- Contratos claros e formais (OpenAPI, protobuf, schema GraphQL)
- Compatibilidade evolutiva e versionamento quando aplicável
- Não misturar semânticas de REST, gRPC e GraphQL

#### web/api/ — REST/HTTP
- Design orientado a recursos, verbos HTTP e status codes corretos
- OpenAPI como contrato formal, RFC 9457 / Problem Details para erros
- Paginação, filtro e ordenação padronizados

#### web/grpc/
- Protobuf-first, backward compatibility, numeração de campos estável
- Deadlines/timeouts explícitos
- Mapeamentos compartilhados em `core/mapper/`

#### web/graphql/
- Schema claro e estável, controle de profundidade e complexidade
- Mitigação de N+1, paginação cursor-based quando fizer sentido

### message/

Borda assíncrona organizada por broker/tecnologia:
- `message/kafka/`, `message/sqs/`, `message/queue/`
- Subpacotes: `consumer/`, `producer/`, `event/`, `header/`, `exception/`

Regras mandatórias:
- Orientada a eventos, **NÃO** a request/response
- Não usar `request/`, `response/`, `model/` ou `mapper/` dentro de `message/`
- Nomenclatura de pacotes: `consumer/`, `producer/` (estável)
- Nomenclatura de classes: idiomática da tecnologia

Requisitos para sistema crítico:
- Idempotência, deduplicação, ordering quando aplicável
- Retry com backoff e jitter, DLQ, poison message handling
- Tracing, métricas, correlação, concorrência segura

### core/

Componentes técnicos compartilhados e reutilizáveis.
**NÃO é domínio. NÃO deve concentrar regra de negócio. NÃO deve virar depósito genérico.**

### domain/

Entidades, serviços de domínio, contratos de repositório, eventos e exceções de domínio.

### infrastructure/

Detalhes técnicos e operacionais: datastore, resilience, logging, metrics, openapi, web, async, availability, messaging.

---

## Ordem Padrão de Consulta dos Papéis

O `staff-engineer-orchestrator` deve consultar nesta ordem:

1. `tech-lead-reviewer` — pragmatismo, simplicidade, manutenibilidade
2. `architect-reviewer` — arquitetura, boundaries, trade-offs, resiliência
3. `api-contract-reviewer` — contratos de borda, breaking changes, schema governance
4. `security-reviewer` — segurança, hardening, superfícies de abuso
5. `ad-dba-reviewer` — dados, persistência, modelagem, queries
6. `software-engineer` — implementação mínima correta
7. `sre-platform-engineer` — operação, deploy, observabilidade, IaC
8. `qa-quality-engineer` — testes, qualidade, edge cases, regressões
9. `performance-reliability-reviewer` — throughput, latência, escalabilidade

---

## Checklist Transversal Obrigatório

### Resiliência e confiabilidade
- [ ] Timeout explícito
- [ ] Retry com backoff e jitter (somente quando faz sentido)
- [ ] Circuit breaker
- [ ] Bulkhead / limitação de concorrência
- [ ] Proteção contra falhas em cascata
- [ ] Degradação controlada
- [ ] Comportamento seguro sob falha parcial e sob carga

### Observabilidade
- [ ] Logs estruturados
- [ ] Métricas técnicas e operacionais
- [ ] Tracing distribuído quando aplicável

### Operabilidade
- [ ] Readiness / liveness consistentes
- [ ] Rollback previsível
- [ ] Execução local reprodutível (Docker + LocalStack)
- [ ] Cloud-readiness para AWS

### Segurança
- [ ] Autenticação e autorização
- [ ] Sem segredos hardcoded
- [ ] Sem dados sensíveis em logs
- [ ] Hardening de bordas

### Testes
- [ ] JUnit 5, PIT, ArchUnit, Testcontainers
- [ ] Testes de contrato, borda web, borda assíncrona
- [ ] Testes de comportamento em falha

### Contratos de borda
- [ ] Compatibilidade evolutiva (OpenAPI, Protobuf, GraphQL Schema, Avro, AsyncAPI)
- [ ] Breaking changes identificados e justificados
- [ ] Schema governance e versionamento

### Dados e persistência
- [ ] Trade-offs relacional vs não relacional, CAP theorem
- [ ] Índices, queries, paginação, concorrência

### Infraestrutura como código
- [ ] Terraform quando aplicável
- [ ] Módulos, variáveis e outputs organizados

---

## Regras Obrigatórias de Execução

1. Toda demanda não trivial passa pelo `staff-engineer-orchestrator` antes de implementação.
2. O orquestrador consulta os papéis relevantes antes de decidir.
3. Nenhum papel implementa mudanças grandes sem análise consolidada.
4. O orquestrador consolida achados, resolve conflitos e define o plano final.
5. Riscos devem ser explícitos e diferenciados (crítico vs melhoria futura).
6. Toda proposta deve respeitar o framework impactado e seu estilo idiomático.
7. Preservar a arquitetura existente — não mover sem justificativa.
8. Preferir a menor estrutura correta, sustentável e profissional.
9. Não criar complexidade desnecessária.
10. Não alterar código existente sem necessidade.

---

## Regras por Framework

### Java 25
Recursos modernos quando agregarem clareza. Considerar concorrência, memória, startup.

### Spring Boot
Idiomatismo Spring, configuração clara, testabilidade forte.

### Quarkus
Startup rápido, footprint reduzido, build-time optimizations.

### Micronaut
DI idiomática, eficiência de memória, inicialização eficiente.

### AWS
Operação em cloud, serviços gerenciados, segurança operacional.

### LocalStack
Testes e desenvolvimento local, reprodutibilidade.

### Docker
Ambiente local reprodutível, paridade com cloud.

### Terraform
Módulos organizados, separação por ambiente, naming consistente.

---

## Como usar com GitHub Copilot

### Para demandas não triviais

Cole no prompt do Copilot:

```
Siga as instruções de docs/ai/orchestration/staff-engineer-orchestrator.md
como papel principal. Consulte os papéis em docs/ai/roles/ conforme a ordem
definida em .github/copilot-instructions.md. Consolide a resposta no formato
de saída obrigatório do orquestrador (16 seções).

Demanda: [descreva aqui]
```

### Para análise focada

```
Siga as instruções de docs/ai/roles/security-reviewer.md e revise [contexto].
```

### Para implementação direta (tarefas triviais)

```
Siga as instruções de docs/ai/roles/software-engineer.md e implemente [tarefa].
```
