# CLAUDE.md — Projeto Multi-Agente (Sistema Crítico)

## Agente Principal

O agente padrão deste projeto é o **staff-engineer-orchestrator**.

Toda demanda não trivial deve passar pelo orquestrador antes de qualquer implementação.
O orquestrador consulta os especialistas, consolida achados, resolve conflitos e entrega o plano final.

**Ninguém deve sair implementando sem análise adequada.**

---

## Stack Oficial

| Camada | Tecnologias |
|--------|------------|
| Linguagens backend | Java 25 · Python · Go |
| Frameworks Java | Spring Boot, Quarkus, Micronaut |
| Jakarta EE / MicroProfile | Jakarta EE 11 · MicroProfile 7.0 · WildFly · Open Liberty · Payara · TomEE |
| Python | pyproject.toml, src layout, pytest, Ruff |
| Go | go.mod, cmd/internal, interfaces idiomáticas |
| Frontend | React (Vite + TypeScript) · Angular (versão atual, Standalone + Signals) · AngularJS (legado/migração) |
| Mobile | Android (Kotlin + Jetpack Compose) · iOS (Swift + SwiftUI) |
| Cloud | AWS (Lambda, API Gateway, EventBridge, SQS, SNS, Step Functions, DynamoDB, S3, ECS) |
| Emulação local | Ministack (drop-in LocalStack replacement, porta 4566) |
| Containerização | Docker |
| IaC | Terraform |
| Ambiente dev | Dev Container (opcional recomendado) |
| Testes Java | JUnit 5, PIT (mutação), ArchUnit (arquitetura), Testcontainers (integração) |
| Testes Python | pytest, fixtures, parametrize |
| Testes Go | testing, table-driven, -race, testcontainers-go |
| Testes Frontend | Jest, Testing Library, Playwright, MSW |
| Testes Mobile | JUnit + Compose Test + Espresso (Android) · XCTest + XCUITest (iOS) |

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

Representa a borda síncrona da aplicação. Pode conter:

- `api/` — REST/HTTP (controllers, request, response, exception)
- `grpc/` — gRPC (service, interceptor, exception)
- `graphql/` — GraphQL (resolver, input, output, exception)

Regras mandatórias para `web/`:
- Separação clara entre borda e domínio
- DTOs próprios por protocolo — não expor entidades de domínio
- Tratamento consistente de erro por protocolo
- Validação de entrada
- Observabilidade e segurança de borda
- Contratos claros e formais (OpenAPI, protobuf, schema GraphQL)
- Compatibilidade evolutiva e versionamento quando aplicável
- Idempotência, paginação, filtros e ordenação quando aplicável
- Não misturar semânticas de REST, gRPC e GraphQL na mesma estrutura

#### web/api/ — REST/HTTP
- Design orientado a recursos
- Verbos HTTP e status codes com semântica correta
- OpenAPI como contrato formal
- RFC 9457 / Problem Details para erros
- Paginação, filtro e ordenação padronizados
- URIs consistentes, payloads estáveis e previsíveis
- Evitar tunneling semântico via POST

#### web/grpc/
- Protobuf-first / contrato primeiro
- Backward compatibility do schema protobuf
- Numeração de campos estável
- Deadlines/timeouts explícitos
- Mapeamentos compartilhados em `core/mapper/`, não em `web/grpc/`

#### web/graphql/
- Schema claro e estável
- Controle de profundidade e complexidade de query
- Mitigação de N+1
- Paginação cursor-based quando fizer sentido
- Separação entre resolver e domínio

### message/

Representa a borda assíncrona da aplicação. Organizada por broker/tecnologia:

- `message/kafka/` — consumer, producer, event, header, exception
- `message/sqs/` — consumer, producer, event, header, exception
- `message/queue/` — consumer, producer, event, header, exception

Regras mandatórias:
- Orientada a eventos, **NÃO** a request/response
- Não usar `request/`, `response/`, `model/` ou `mapper/` dentro de `message/`
- Mapeamentos compartilhados ficam em `core/mapper/`
- Nomenclatura de pacotes: `consumer/`, `producer/` (estável)
- Nomenclatura de classes: idiomática da tecnologia (Kafka: Consumer/Producer, SQS: Listener/Sender)

Requisitos de mensageria para sistema crítico:
- Idempotência e deduplicação
- Ordering quando aplicável
- Retry com backoff e jitter
- DLQ e poison message handling
- Timeout e correlação de mensagens
- Tracing e métricas (consumo, falha, retry, lag, latência)
- Concorrência segura
- Compatibilidade de payload, evento e header
- Proteção contra flood/reprocessamento descontrolado

### core/

Componentes técnicos compartilhados e reutilizáveis:
- Annotations customizadas
- Validações compartilhadas
- Mappers reutilizáveis
- Suporte transversal a métricas
- Helpers e componentes técnicos comuns

**core/ NÃO é domínio. NÃO deve concentrar regra de negócio. NÃO deve virar depósito genérico.**

### domain/

- Entidades
- Serviços de domínio
- Contratos de repositório
- Eventos de domínio
- Exceções de domínio

### infrastructure/

Detalhes técnicos, configuração, integrações com plataforma:
- `datastore/` — persistência
- `resilience/` — circuit breaker, retry, bulkhead
- `logging/` — logs estruturados
- `metrics/` — métricas operacionais
- `openapi/` — configuração OpenAPI
- `web/` — configuração web
- `async/` — configuração assíncrona
- `availability/` — readiness/liveness
- `messaging/` — detalhe técnico dos brokers (configuração, serialização, infraestrutura de transporte)

### iac/terraform/

Infraestrutura como código:
- Módulos, ambientes, variáveis, outputs
- Naming consistente
- Separação por ambiente quando fizer sentido
- Clareza operacional e manutenção simples

### .devcontainer/ (opcional recomendado)

Padronização do ambiente de desenvolvimento local quando agregar valor sem complexidade excessiva.

---

## Estrutura Conceitual de Referência

```
<project-root>/
├─ src/main/java/<base-package>/
│  ├─ Application.java
│  ├─ web/
│  │  ├─ api/ (controller, request, response, exception)
│  │  ├─ grpc/ (service, interceptor, exception)
│  │  └─ graphql/ (resolver, input, output, exception)
│  ├─ message/
│  │  ├─ kafka/ (consumer, producer, event, header, exception)
│  │  ├─ sqs/ (consumer, producer, event, header, exception)
│  │  └─ queue/ (consumer, producer, event, header, exception)
│  ├─ core/ (annotation, validation, mapper, metrics, support)
│  ├─ domain/ (entity, repository, service, event, exception)
│  └─ infrastructure/
│     ├─ datastore/
│     ├─ resilience/
│     ├─ logging/
│     ├─ metrics/
│     ├─ openapi/
│     ├─ web/
│     ├─ async/
│     ├─ availability/
│     └─ messaging/
├─ src/main/resources/
│  ├─ application.yml / application-local.yml / application-test.yml
│  ├─ logback-spring.xml
│  ├─ db/migration/{vendor}
│  ├─ openapi/ / protobuf/ / graphql/ / asyncapi/ / messaging/
├─ src/test/
│  ├─ java/...
│  └─ resources/ (features, contracts, payloads, fixtures, messaging)
├─ iac/terraform/
└─ .devcontainer/ (opcional)
```

---

## Checklist Transversal Obrigatório

Toda proposta, revisão ou implementação deve validar:

### Resiliência e confiabilidade
- [ ] Timeout explícito
- [ ] Retry com backoff e jitter (somente quando faz sentido)
- [ ] Circuit breaker
- [ ] Bulkhead / limitação de concorrência
- [ ] Proteção contra falhas em cascata
- [ ] Degradação controlada
- [ ] Comportamento seguro sob falha parcial
- [ ] Comportamento seguro sob carga

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
- [ ] JUnit 5 como base
- [ ] Testes de mutação (PIT)
- [ ] Testes de arquitetura (ArchUnit)
- [ ] Testes de integração (Testcontainers)
- [ ] Testes de contrato
- [ ] Testes de borda web e assíncrona
- [ ] Testes de comportamento em falha

### Dados e persistência
- [ ] Trade-offs relacional vs não relacional
- [ ] CAP theorem quando aplicável
- [ ] Índices e otimização de queries
- [ ] Paginação e concorrência
- [ ] Aderência ao ecossistema AWS

### Contratos de borda
- [ ] Compatibilidade evolutiva (OpenAPI, Protobuf, GraphQL Schema, Avro, AsyncAPI)
- [ ] Breaking changes identificados e justificados
- [ ] Schema governance e versionamento
- [ ] Testes de contrato
- [ ] Schema Registry configurado (quando Avro/Protobuf)

### Infraestrutura como código
- [ ] Terraform quando aplicável
- [ ] Módulos, variáveis e outputs organizados
- [ ] Separação por ambiente quando fizer sentido

### Versões de dependências
- [ ] Versão do framework (Spring Boot, Quarkus, Micronaut, Jakarta EE, MicroProfile) verificada via WebSearch — não por memória
- [ ] Versão é GA (não RC, SNAPSHOT, M1, M2, Alpha, Beta)
- [ ] Compatibilidade com Java 25 confirmada
- [ ] Sem dependências com CVE crítico ou alto conhecidos
- [ ] Sem dependências com EOL declarado

### Compliance e proteção de dados
- [ ] Dados pessoais mapeados (LGPD/GDPR)
- [ ] Base legal para tratamento identificada
- [ ] Dados pessoais ausentes de logs, traces e métricas
- [ ] Residência de dados alinhada com região AWS (sa-east-1 para Brasil)
- [ ] Retenção e descarte de dados pessoais definidos

### FinOps (custo AWS)
- [ ] Retenção de logs CloudWatch definida
- [ ] Rightsizing de instâncias/containers avaliado
- [ ] Tags de custo (cost allocation tags) nas resources Terraform
- [ ] Sem anti-padrões de billing críticos (NAT Gateway desnecessário, logs ilimitados, etc.)

### Experiência do desenvolvedor
- [ ] Onboarding documentado (máximo 3-5 comandos para rodar localmente)
- [ ] docker-compose sobe todos os serviços necessários
- [ ] application-local.yml completo e funcional
- [ ] Ministack cobre os serviços AWS usados localmente

### CI/CD e deploy
- [ ] Pipeline CI: lint → test → build → package (jobs separados)
- [ ] Pipeline CD: pull-artifact → terraform-plan → approval → terraform-apply → deploy → smoke-test
- [ ] OIDC para AWS — sem credenciais de longa duração em CI
- [ ] Lambda versions e aliases usados — não deploy direto em `$LATEST`
- [ ] Canary ou blue/green para produção Lambda
- [ ] Rollback documentado e testável em menos de 5 minutos
- [ ] Terraform state em S3 com DynamoDB lock

### SLOs, observabilidade e incident response
- [ ] SLOs definidos por componente crítico
- [ ] SLIs mapeados para métricas AWS reais
- [ ] CloudWatch Alarms configurados para SLO breach
- [ ] Runbook para cada alarme crítico
- [ ] Template de postmortem definido
- [ ] On-call e escalada documentados

---

## Regra de Versões de Dependências

**Nenhum agente pode assumir versão de dependência por memória ou knowledge cutoff.**

Sempre que houver criação ou modificação de `pom.xml`, `build.gradle`, `pyproject.toml`, `go.mod`, Terraform `required_providers` ou qualquer referência a framework/dependência/imagem Docker, o `dependency-versions-reviewer` deve ser acionado **antes** do `software-engineer`. Ele usa WebSearch para verificar a versão GA mais recente.

- Nunca usar versões RC, SNAPSHOT, M1, M2, Alpha ou Beta em sistemas críticos
- Sempre confirmar se a versão é GA e tem suporte ativo
- O knowledge cutoff do modelo pode estar desatualizado — WebSearch é a fonte verdade
- Inclui Terraform providers (`hashicorp/aws ~> X.Y`) e Docker base images (tag específica, não `latest`)

---

## Ordem Padrão de Consulta dos Agentes

O `staff-engineer-orchestrator` deve consultar os agentes nesta ordem preferencial:

0. `dependency-versions-reviewer` — **OBRIGATÓRIO** quando há dependências envolvidas: valida versões GA mais recentes via WebSearch antes de qualquer implementação
1. `tech-lead-reviewer` — pragmatismo, simplicidade, manutenibilidade
2. `architect-reviewer` — arquitetura, boundaries, trade-offs, resiliência
3. `api-contract-reviewer` — contratos de borda, breaking changes, schema governance
4. `security-reviewer` — segurança, hardening, superfícies de abuso
5. `compliance-reviewer` — LGPD, GDPR, residência de dados, direitos do titular
6. `ad-dba-reviewer` — dados, persistência, modelagem, queries
7. `data-engineering-aws-architect` — *(quando há pipelines de dados, ETL/ELT, data lake, streaming, Glue, EMR, Kinesis, Athena)* decisão arquitetural de dados
8. `java-specialist` — *(quando stack Java com Spring Boot, Quarkus ou Micronaut)* estrutura, idiomatismo, ecossistema Java 25 + framework
8. `jakarta-ee-specialist` — *(quando stack Jakarta EE, Java EE, MicroProfile ou servidor de aplicação certificado)* CDI, JAX-RS, JPA, JMS, MicroProfile FT/Config/Health — WildFly, Open Liberty, Payara, TomEE
8. `python-specialist` — *(quando stack Python)* estrutura, idiomatismo, ecossistema Python
8. `go-specialist` — *(quando stack Go)* estrutura, idiomatismo, ecossistema Go
8. `frontend-specialist` — *(quando stack contém React, Angular ou AngularJS)* estrutura, idiomatismo, performance, a11y, testes frontend
8. `mobile-native-specialist` — *(quando stack contém Android ou iOS nativos)* arquitetura, idiomatismo Kotlin/Swift, segurança mobile, CI/CD de store
9. `software-engineer` — implementação mínima correta (após versões validadas)
10. `sre-platform-engineer` — operação, deploy, observabilidade, IaC
11. `cicd-pipeline-engineer` — *(quando há pipeline CI/CD, deploy strategy Lambda, Terraform em CI)* GitHub Actions, deploy blue/green/canary, rollback, quality gates
12. `incident-response-reviewer` — *(quando o sistema vai para produção ou há SLAs definidos)* SLOs/SLIs, runbooks, postmortem, chaos engineering
13. `finops-reviewer` — custo AWS, rightsizing, anti-padrões de billing
14. `devex-reviewer` — onboarding, ambiente local, docker-compose, Dev Container (poliglota)
15. `qa-quality-engineer` — testes, qualidade, edge cases, regressões
16. `performance-reliability-reviewer` — throughput, latência, escalabilidade
17. `tech-writer` — *(quando há mudança de comportamento, novo componente ou documentação desatualizada)* README, getting-started, testing, troubleshooting, ADRs, diagramas C4

---

## Regras Obrigatórias de Execução

1. Toda demanda não trivial passa pelo `staff-engineer-orchestrator` antes de implementação.
2. O orquestrador consulta os especialistas relevantes antes de decidir.
3. Nenhum agente implementa sem análise adequada.
4. O orquestrador consolida achados, resolve conflitos e define o plano final.
5. A resposta final segue o formato estruturado definido no orquestrador.
6. Riscos devem ser explícitos e diferenciados (crítico vs melhoria futura).
7. Toda proposta deve respeitar o framework impactado e seu estilo idiomático.
8. Preservar a arquitetura existente — não mover sem justificativa.
9. Preferir a menor estrutura correta, sustentável e profissional.
10. Não criar complexidade desnecessária.

---

## Regras por Framework

### Java 25
- Recursos modernos quando agregarem clareza e segurança
- Considerar concorrência, memória, startup e desempenho

### Spring Boot
- Idiomatismo Spring, configuração clara, testabilidade forte
- Boas práticas de web, bean lifecycle, exception handling, observability, messaging

### Quarkus
- Startup rápido, footprint reduzido, build-time optimizations

### Micronaut
- DI idiomática, eficiência de memória, inicialização eficiente

### AWS
- Operação em cloud, serviços gerenciados, segurança operacional

### LocalStack
- Testes e desenvolvimento local, reprodutibilidade

### Docker
- Ambiente local reprodutível, paridade com cloud

### Terraform
- Módulos organizados, separação por ambiente, naming consistente

### Ministack
- Drop-in replacement de LocalStack — mesma interface, porta 4566
- Healthcheck em `/_ministack/health`
- Não suporta init-scripts via `ready.d` — inicialização via Makefile/scripts externos

---

## Estrutura do Monorepo

```
poc-aws-lambda/
├── lambdas/
│   ├── lambda-java-quarkus/       # Java 25 + Quarkus
│   ├── lambda-java-spring/        # Java 25 + Spring Boot
│   ├── lambda-java-micronaut/     # Java 25 + Micronaut
│   ├── lambda-go/                 # Go
│   └── lambda-python/             # Python
├── iac/
│   └── terraform/
│       ├── modules/               # módulos reutilizáveis (lambda, sqs, dynamodb, sns)
│       └── environments/          # dev, staging, prod
├── docs/
│   ├── architecture/
│   │   ├── adr/                   # Architecture Decision Records
│   │   └── diagrams/              # Diagramas C4
│   ├── getting-started.md
│   ├── local-development.md
│   └── troubleshooting.md
├── .github/
│   └── workflows/                 # GitHub Actions
├── .claude/
│   └── agents/                    # Agentes especializados
├── docker-compose.yml             # Ministack + dependências locais
├── Makefile                       # Targets: build, test, deploy, local
└── CLAUDE.md
```

---

## ADRs — Decisões Arquiteturais

Decisões arquiteturais significativas devem ser documentadas em `docs/architecture/adr/`. Ver template no `tech-writer` agent.

Exemplos de ADRs que devem existir neste projeto:
- ADR-0001: Escolha de DynamoDB para persistência de pedidos
- ADR-0002: Uso de SQS + Lambda para processamento assíncrono
- ADR-0003: ReportBatchItemFailures + DLQ como estratégia de error handling
- ADR-0004: Ministack como emulador local de AWS
