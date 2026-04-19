# AGENTS.md — Projeto Multi-Agente (Sistema Crítico)

> Este arquivo é lido automaticamente pelo **Devin CLI** (e outros agentes que suportam o padrão AGENTS.md) no início de toda sessão.

## Agente Principal

O agente padrão deste projeto é o **staff-engineer-orchestrator** (subagent definido em `.devin/agents/staff-engineer-orchestrator/AGENT.md`).

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
| Frontend | React (Vite + TS) · Angular (Standalone + Signals) · AngularJS (migração) |
| Mobile | Android (Kotlin + Compose) · iOS (Swift + SwiftUI) |
| Cloud | AWS (Lambda, API Gateway, EventBridge, SQS, SNS, Step Functions, DynamoDB, S3, ECS) |
| Emulação local | Floci (porta 4566) |
| Containerização | Docker |
| IaC | Terraform |

---

## Contexto de Sistema Crítico

Todo código, análise, revisão e proposta deve considerar como requisito transversal:

- Resiliência máxima · Confiabilidade máxima · Operabilidade máxima
- Observabilidade forte (logs estruturados, métricas, tracing distribuído)
- Segurança forte
- Comportamento seguro sob falha parcial e sob carga
- Menor risco possível de produção

---

## Organização Arquitetural

### Regras de bordas

| Camada | Tipo | Descrição |
|--------|------|-----------|
| `web/` | Borda síncrona | Entrada/saída síncrona (REST, gRPC, GraphQL) |
| `message/` | Borda assíncrona | Entrada/saída orientada a eventos (Kafka, SQS, filas) |

Ambas ficam no mesmo nível estrutural. `message/` **NÃO** fica dentro de `infrastructure/`.

### Outras camadas

- `core/` — componentes técnicos compartilhados (annotations, validações, mappers, métricas). **Não é domínio.**
- `domain/` — entidades, serviços de domínio, contratos de repositório, eventos, exceções.
- `infrastructure/` — detalhes técnicos (datastore, resilience, logging, metrics, openapi, web, async, availability, messaging).
- `iac/terraform/` — IaC.

---

## Checklist Transversal Obrigatório

Toda proposta, revisão ou implementação deve validar:

### Resiliência e confiabilidade
- [ ] Timeout explícito · Retry com backoff e jitter · Circuit breaker
- [ ] Bulkhead · Proteção contra falhas em cascata · Degradação controlada

### Observabilidade
- [ ] Logs estruturados · Métricas técnicas e operacionais · Tracing distribuído

### Operabilidade
- [ ] Readiness/liveness · Rollback previsível · Execução local reprodutível (Docker + Floci) · Cloud-readiness AWS

### Segurança
- [ ] Autenticação/autorização · Sem segredos hardcoded · Sem dados sensíveis em logs · Hardening de bordas

### Testes
- [ ] JUnit 5 · Testes de mutação (PIT) · ArchUnit · Testcontainers · Contrato · Borda · Falha

### Dados
- [ ] Trade-offs relacional/não relacional · CAP · Índices · Paginação · Aderência AWS

### Contratos de borda
- [ ] Compatibilidade evolutiva · Breaking changes justificados · Schema governance · Schema Registry

### Versões de dependências
- [ ] Verificadas via WebSearch — não por memória
- [ ] GA (não RC, SNAPSHOT, M1, M2, Alpha, Beta) · Java 25 compatível · Sem CVE crítico · Sem EOL

### Compliance
- [ ] Dados pessoais mapeados (LGPD/GDPR) · Base legal · Ausentes de logs · Região alinhada · Retenção definida

### FinOps
- [ ] Retenção CloudWatch definida · Rightsizing · Cost tags · Sem anti-padrões de billing

### CI/CD e deploy
- [ ] Pipeline CI: lint→test→build→package · Pipeline CD: pull-artifact→plan→approval→apply→deploy→smoke
- [ ] OIDC para AWS · Lambda versions+aliases · Canary/blue-green · Rollback <5min · Terraform state em S3 + DynamoDB lock

### SLOs e incident response
- [ ] SLOs/SLIs definidos · CloudWatch Alarms · Runbook por alarme · Template de postmortem · On-call documentado

---

## Regra de Versões de Dependências

**Nenhum agente pode assumir versão de dependência por memória ou knowledge cutoff.**

Sempre que houver mudança em `pom.xml`, `build.gradle`, `pyproject.toml`, `go.mod`, providers Terraform ou imagens Docker, o `dependency-versions-reviewer` deve ser acionado **antes** do `software-engineer`. Ele usa WebSearch para verificar a versão GA mais recente.

---

## Ordem Padrão de Consulta

O `staff-engineer-orchestrator` delega subagentes nesta ordem preferencial:

0. `dependency-versions-reviewer` — **OBRIGATÓRIO** quando há dependências
1. `tech-lead-reviewer`
2. `architect-reviewer`
3. `api-contract-reviewer`
4. `security-reviewer`
5. `compliance-reviewer`
6. `ad-dba-reviewer`
7. `data-engineering-aws-architect` *(quando pipelines de dados)*
8. Especialistas de stack: `java-specialist` · `jakarta-ee-specialist` · `python-specialist` · `go-specialist` · `frontend-specialist` · `mobile-native-specialist`
9. `software-engineer` (após versões validadas)
10. `sre-platform-engineer`
11. `cicd-pipeline-engineer` *(quando CI/CD)*
12. `incident-response-reviewer` *(quando produção)*
13. `finops-reviewer`
14. `devex-reviewer`
15. `qa-quality-engineer`
16. `performance-reliability-reviewer`
17. `tech-writer` *(quando documentação)*

---

## Regras Obrigatórias de Execução

1. Toda demanda não trivial passa pelo `staff-engineer-orchestrator` antes de implementação.
2. O orquestrador consulta os especialistas relevantes antes de decidir.
3. Nenhum agente implementa sem análise adequada.
4. O orquestrador consolida achados, resolve conflitos e define o plano final.
5. Riscos explícitos e diferenciados (crítico vs melhoria futura).
6. Toda proposta deve respeitar o framework impactado e seu estilo idiomático.
7. Preservar a arquitetura existente — não mover sem justificativa.
8. Preferir a menor estrutura correta, sustentável e profissional.
9. Não criar complexidade desnecessária.

---

## Pontos de extensão

| Extensão | Onde fica |
|----------|-----------|
| Subagente | `.devin/agents/<nome>/AGENT.md` |
| Skill / slash command | `.devin/skills/<nome>/SKILL.md` |
| Permissões + hooks | `.devin/config.json` |
| Overrides pessoais (gitignored) | `.devin/config.local.json` |

Consulte o `README.md` deste diretório para passo a passo completo.
