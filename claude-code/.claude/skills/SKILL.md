# Skills Index

Skills globais disponíveis em todos os projetos. Carregam on-demand quando relevantes ou via `/skill-name`.

## Java
- [java-project-setup](java-project-setup.md) — Estrutura, records, virtual threads, Spring Boot config, ArchUnit
- [java-spring-patterns](java-spring-patterns.md) — Resilience4j, Security JWT, Kafka/SQS, caching, scheduling
- [java-testing](java-testing.md) — JUnit 5, Testcontainers, MockMvc, ArchUnit, PIT mutacao
- [java-quarkus-patterns](java-quarkus-patterns.md) — Quarkus dev mode, CDI, RESTEasy, native build, Lambda
- [java-micronaut-patterns](java-micronaut-patterns.md) — Micronaut DI, HTTP client, GraalVM, Lambda
- [jakarta-ee-patterns](jakarta-ee-patterns.md) — CDI, JAX-RS, JPA, JMS, MicroProfile FT/Config/Health

## Go
- [go-project-setup](go-project-setup.md) — cmd/internal layout, interfaces, slog, functional options
- [go-web-frameworks](go-web-frameworks.md) — Gin, Chi, Echo: routing, middleware, validation, graceful shutdown
- [go-testing](go-testing.md) — Table-driven, Testcontainers, httptest, benchmarks, race detection

## Python
- [python-project-setup](python-project-setup.md) — src layout, pyproject.toml, FastAPI, structlog, Ruff
- [python-fastapi-patterns](python-fastapi-patterns.md) — Pydantic v2, async, DI, middleware, OpenAPI, SQLAlchemy async
- [python-testing](python-testing.md) — pytest fixtures, parametrize, AsyncMock, Testcontainers

## Frontend
- [react-patterns](react-patterns.md) — Hooks, React Query, Zustand, Testing Library, Vite
- [angular-patterns](angular-patterns.md) — Standalone Components, Signals, inject(), HttpClient, RxJS
- [angularjs-migration](angularjs-migration.md) — ngUpgrade, dual-boot, strangler fig, migracao incremental

## Mobile
- [android-patterns](android-patterns.md) — Kotlin, Jetpack Compose, MVVM, Hilt, Room, Coroutines
- [ios-patterns](ios-patterns.md) — Swift, SwiftUI, @Observable, async/await, SwiftData, Navigation

## AWS
- [aws-architecture-patterns](aws-architecture-patterns.md) — API GW+Lambda, SQS+Lambda, EventBridge, Step Functions, DynamoDB
- [aws-iac-patterns](aws-iac-patterns.md) — Terraform multi-env, remote state, modulos, IAM, alarmes
- [aws-lambda-checklist](aws-lambda-checklist.md) — Handler, IAM, cold start, deploy, DLQ, observabilidade
- [aws-observability](aws-observability.md) — CloudWatch, X-Ray, Log Insights, dashboards, alerting

## Data Engineering
- [spark-data-engineering](spark-data-engineering.md) — PySpark, batch, streaming, Glue, EMR, data quality

## Contratos e Comunicacao
- [api-design](api-design.md) — REST best practices: URLs, methods, status codes, paginacao, erros
- [grpc-patterns](grpc-patterns.md) — Protobuf, service definition, streaming, deadlines, interceptors
- [graphql-patterns](graphql-patterns.md) — Schema design, resolvers, N+1, DataLoader, pagination
- [async-messaging-patterns](async-messaging-patterns.md) — SQS, Kafka, EventBridge, idempotencia, DLQ, ordering

## QA e Processo
- [qa-process](qa-process.md) — Piramide de testes, criterios de aceite, edge cases, quality gates
- [software-engineering-process](software-engineering-process.md) — Design, code review, CI/CD, deploy, SLOs
- [testing-strategies](testing-strategies.md) — Estrategia por tipo de codigo, exemplos por linguagem
- [performance-testing](performance-testing.md) — k6, Gatling, JMH, load testing, benchmarks, profiling

## Arquitetura e Documentacao
- [c4-model](c4-model.md) — Context, Container, Component, Code + Structurizr, Mermaid
- [adr-template](adr-template.md) — ADR: template, quando criar, exemplos, boas praticas
- [twelve-factor-app](twelve-factor-app.md) — 12 fatores, cloud-native, config, stateless, logs

## Transversal
- [code-review](code-review.md) — Revisao estruturada: correcao, seguranca, qualidade, testes
- [commit-message](commit-message.md) — Conventional Commits com exemplos
- [pr-description](pr-description.md) — Template de PR: summary, changes, test plan
- [security-audit](security-audit.md) — Auditoria: segredos, injection, auth, dados, deps
- [error-handling](error-handling.md) — Tratamento de erros por linguagem, RFC 9457
- [dockerfile-best-practices](dockerfile-best-practices.md) — Multi-stage, seguranca, cache, templates por linguagem
- [git-workflow](git-workflow.md) — Merge conflicts, rebase, cherry-pick, bisect, recovery
- [terraform-module](terraform-module.md) — Estrutura, variables, outputs, naming, state, seguranca
- [observability-setup](observability-setup.md) — Logs, metricas RED/USE, tracing, OpenTelemetry
- [database-migration](database-migration.md) — Zero-downtime, expand-contract, backfill, rollback
- [dependency-upgrade](dependency-upgrade.md) — Processo seguro de upgrade por ecossistema
