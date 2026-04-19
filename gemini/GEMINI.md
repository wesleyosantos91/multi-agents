# GEMINI.md — Projeto Multi-Agente (Sistema Crítico)

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
| Emulação local | LocalStack / Floci (emulador AWS local, porta 4566) |
| Containerização | Docker |
| IaC | Terraform |
| Testes Java | JUnit 5, PIT (mutação), ArchUnit (arquitetura), Testcontainers (integração) |
| Testes Python | pytest, fixtures, parametrize |
| Testes Go | testing, table-driven, -race, testcontainers-go |
| Testes Frontend | Jest, Testing Library, Playwright, MSW |

---

## Contexto de Sistema Crítico

Este é um sistema crítico. Todo código, análise, revisão e proposta deve considerar como requisito transversal:

- Resiliência máxima e Confiabilidade (Circuit Breakers, Retries, Timeouts)
- Observabilidade forte (logs estruturados, métricas, tracing distribuído)
- Alta Operabilidade (Cloud-ready, Rollback previsível)
- Segurança forte (Hardening, Proteção de segredos)
- Comportamento seguro sob falha parcial e carga

---

## Organização Arquitetural

### Camadas de Borda (`web/` e `message/`)
- `web/api/`: REST/HTTP (DTOs próprios, RFC 9457 para erros, OpenAPI).
- `web/grpc/`: gRPC (Protobuf-first, backward compatibility).
- `web/graphql/`: GraphQL (Schema-first, mitigação de N+1).
- `message/`: Assíncrona (Kafka, SQS). Idempotência, Dead Letter Queues (DLQ), Retry com Backoff.

### Core, Domain e Infrastructure
- `core/`: Componentes técnicos transversais (NÃO contém regras de negócio).
- `domain/`: Entidades, Serviços de Domínio, Contratos de Repositório.
- `infrastructure/`: Detalhes técnicos (Datastore, Resilience, Cloud Config).

---

## Checklist Transversal Obrigatório

Toda proposta deve validar:
- [ ] **Resiliência:** Timeouts, retries, circuit breakers.
- [ ] **Observabilidade:** Logs estruturados e métricas.
- [ ] **Segurança:** Sem segredos hardcoded, hardening de bordas.
- [ ] **Contratos:** Compatibilidade evolutiva e testes de contrato.
- [ ] **Versões:** Apenas versões **GA** (verificadas via `google_web_search`).
- [ ] **Compliance:** LGPD/GDPR e residência de dados.

---

## Ordem Padrão de Consulta dos Agentes

O `staff-engineer-orchestrator` consulta os agentes nesta ordem:

0. `dependency-versions-reviewer`: Valida versões GA via `google_web_search`.
1. `tech-lead-reviewer`: Pragmatismo e simplicidade.
2. `architect-reviewer`: Arquitetura, trade-offs e resiliência.
3. `api-contract-reviewer`: Contratos e breaking changes.
4. `security-reviewer`: Segurança e hardening.
5. `compliance-reviewer`: LGPD e GDPR.
6. `ad-dba-reviewer`: Persistência e modelagem de dados.
7. `software-engineer`: Implementação técnica.
8. `sre-platform-engineer`: Operabilidade, IaC e Observabilidade.
9. `qa-quality-engineer`: Testes e qualidade.
10. `tech-writer`: Documentação e ADRs.

---

## Comandos Especializados (Slash Commands)

Utilize os comandos para acionar fluxos específicos:
- `/review`: Revisão inteligente da branch.
- `/implement`: Análise e implementação de demanda.
- `/debug`: Investigação de causa raiz e correção.
- `/refactor`: Refatoração segura.
- `/pre-pr`: Checklist final antes de Pull Request.
- `/check-deps`: Validação de versões de dependências.

---

## Regras de Execução

1. Toda demanda não trivial passa pelo orquestrador.
2. O orquestrador consolida achados e define o plano final.
3. Riscos devem ser explícitos e priorizados.
4. Preservar a arquitetura existente — não mover sem justificativa.
5. Preferir a menor estrutura correta e profissional.
