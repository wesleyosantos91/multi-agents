# AGENTS.md — Projeto Multi-Agente via Codex (Sistema Crítico)

## Papel Principal

O papel lógico padrão deste repositório é o **staff-engineer-orchestrator**.

Toda demanda não trivial deve passar pelo orquestrador antes de qualquer implementação.
O orquestrador consulta as skills especializadas, consolida achados, resolve conflitos e entrega o plano final.

**Ninguém deve sair implementando sem análise adequada.**

---

## Stack Oficial

| Camada | Tecnologias |
|--------|------------|
| Linguagens | Java 25 · Python · Go |
| Frameworks Java | Spring Boot, Quarkus, Micronaut |
| Python | pyproject.toml, src layout, pytest, Ruff |
| Go | go.mod, cmd/internal, interfaces idiomáticas |
| Cloud | AWS (Lambda, API Gateway, EventBridge, SQS, SNS, Step Functions, DynamoDB, S3, ECS) |
| Emulação local | LocalStack |
| Containerização | Docker |
| IaC | Terraform |
| Ambiente dev | Dev Container (opcional recomendado) |
| Testes Java | JUnit 5, PIT (mutação), ArchUnit (arquitetura), Testcontainers (integração) |
| Testes Python | pytest, fixtures, parametrize |
| Testes Go | testing, table-driven, -race, testcontainers-go |

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
├─ .agents/skills/
└─ .devcontainer/ (opcional)
```

---

## Skills Disponíveis

As skills especializadas ficam em `.agents/skills/*/SKILL.md`.

Cada skill tem papel, escopo, regras mandatórias, checklist e formato de saída obrigatório.

### Configuração de runtime dos agentes

Cada skill em `.agents/skills/*/SKILL.md` tem um agente de runtime correspondente em `.codex/agents/*.toml`.

Os dois níveis são complementares:

| Nível | Caminho | Função |
|-------|---------|--------|
| Instruções da skill | `.agents/skills/<nome>/SKILL.md` | Papel, escopo, regras, checklist e formato de saída |
| Runtime do agente | `.codex/agents/<nome>.toml` | Modelo, sandbox, instruções de escopo para o Codex CLI |

O `.codex/config.toml` define parâmetros globais:
- `max_threads = 6` — paralelismo máximo de agentes simultâneos
- `max_depth = 1` — hierarquia plana: o orquestrador aciona especialistas, mas especialistas não acionam outros agentes. Intencional — evita recursão e mantém o fluxo previsível.

Prioridade de regras: `AGENTS.md` > `.codex/agents/*.toml` > `.agents/skills/*/SKILL.md`.

---

## Regra de Versões de Dependências

**Nenhuma skill pode assumir versão de dependência por memória ou knowledge cutoff.**

Sempre que houver criação ou modificação de `pom.xml`, `build.gradle`, `pyproject.toml`, `requirements*.txt`, `go.mod` ou qualquer referência a framework/dependência, o `dependency-versions-reviewer` deve ser acionado **antes** do `software-engineer`. Ele usa WebSearch para verificar a versão GA mais recente no Maven Central, PyPI e go.dev.

- Nunca usar versões RC, SNAPSHOT, M1, M2, Alpha ou Beta em sistemas críticos
- Sempre confirmar se a versão é GA e tem suporte ativo
- O knowledge cutoff do modelo pode estar desatualizado — WebSearch é a fonte verdade

---

## Ordem Padrão de Consulta das Skills

O `staff-engineer-orchestrator` deve consultar as skills nesta ordem preferencial:

0. `dependency-versions-reviewer` — **OBRIGATÓRIO** quando há dependências envolvidas: valida versões GA mais recentes via WebSearch antes de qualquer implementação
1. `tech-lead-reviewer` — pragmatismo, simplicidade, manutenibilidade
2. `architect-reviewer` — arquitetura, boundaries, trade-offs, resiliência
3. `api-contract-reviewer` — contratos de borda, breaking changes, schema governance
4. `security-reviewer` — segurança, hardening, superfícies de abuso
5. `compliance-reviewer` — LGPD, GDPR, residência de dados, direitos do titular
6. `ad-dba-reviewer` — dados, persistência, modelagem, queries
7. `data-engineering-aws-architect` — *(quando há pipelines de dados, ETL/ELT, data lake, streaming, Glue, EMR, Kinesis, Athena)* decisão arquitetural de dados
8. `java-specialist` — *(quando stack Java)* estrutura, idiomatismo, ecossistema Java 25 + framework
8. `python-specialist` — *(quando stack Python)* estrutura, idiomatismo, ecossistema Python
8. `go-specialist` — *(quando stack Go)* estrutura, idiomatismo, ecossistema Go
9. `software-engineer` — implementação mínima correta (após versões validadas)
10. `sre-platform-engineer` — operação, deploy, observabilidade, IaC
11. `finops-reviewer` — custo AWS, rightsizing, anti-padrões de billing
12. `devex-reviewer` — onboarding, ambiente local, docker-compose, Dev Container (poliglota)
13. `qa-quality-engineer` — testes, qualidade, edge cases, regressões
14. `performance-reliability-reviewer` — throughput, latência, escalabilidade
15. `tech-writer` — *(quando há mudança de comportamento, novo componente ou documentação desatualizada)* README, getting-started, testing, troubleshooting

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
- [ ] JUnit 5 como base (Java)
- [ ] Testes de mutação (PIT) — Java
- [ ] Testes de arquitetura (ArchUnit) — Java
- [ ] Testes de integração (Testcontainers) — Java/Go
- [ ] pytest com fixtures e parametrize — Python
- [ ] table-driven com -race — Go
- [ ] Testes de contrato
- [ ] Testes de borda web e assíncrona
- [ ] Testes de comportamento em falha

### Versões de dependências
- [ ] Versão do framework verificada via WebSearch (não por memória)
- [ ] Versão é GA (não RC, SNAPSHOT, M1, M2, Alpha, Beta)
- [ ] Compatibilidade com a linguagem da stack confirmada
- [ ] Sem dependências com CVE crítico ou alto conhecidos
- [ ] Sem dependências com EOL declarado

### Contratos de borda
- [ ] Compatibilidade evolutiva (OpenAPI, Protobuf, GraphQL Schema, Avro, AsyncAPI)
- [ ] Breaking changes identificados e justificados
- [ ] Schema governance e versionamento
- [ ] Testes de contrato
- [ ] Schema Registry configurado (quando Avro/Protobuf)

### Dados e persistência
- [ ] Trade-offs relacional vs não relacional
- [ ] CAP theorem quando aplicável
- [ ] Índices e otimização de queries
- [ ] Paginação e concorrência
- [ ] Aderência ao ecossistema AWS

### Infraestrutura como código
- [ ] Terraform quando aplicável
- [ ] Módulos, variáveis e outputs organizados
- [ ] Separação por ambiente quando fizer sentido

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
- [ ] Configuração local completa e funcional por linguagem
- [ ] LocalStack cobre os serviços AWS usados localmente

---

## Regras Obrigatórias de Execução

1. Toda demanda não trivial passa pelo `staff-engineer-orchestrator` antes de implementação.
2. O orquestrador consulta as skills relevantes antes de decidir.
3. Nenhuma skill implementa mudanças grandes sem análise consolidada.
4. O orquestrador consolida achados, resolve conflitos e define o plano final.
5. A resposta final segue o formato estruturado definido no orquestrador.
6. Riscos devem ser explícitos e diferenciados (crítico vs melhoria futura).
7. Toda proposta deve respeitar o framework impactado e seu estilo idiomático.
8. Preservar a arquitetura existente — não mover sem justificativa.
9. Preferir a menor estrutura correta, sustentável e profissional.
10. Não criar complexidade desnecessária.

---

## Disciplina Operacional

### Antes de propor mudança
- [ ] Inspecionar estrutura e convenções existentes
- [ ] Identificar arquivos e módulos impactados
- [ ] Verificar se já existe solução equivalente
- [ ] Validar que a mudança é a menor correta

### Durante a implementação
- [ ] Preservar base existente — operar incrementalmente
- [ ] Não alterar código que não precisa mudar
- [ ] Não introduzir dependências sem justificativa
- [ ] Não comprometer backward compatibility sem explicitar impacto
- [ ] Rodar validações locais quando possível

### Antes de encerrar a tarefa
- [ ] Mostrar claramente o que foi criado, alterado e por quê
- [ ] Indicar comandos de validação
- [ ] Revisar riscos remanescentes
- [ ] Confirmar estratégia de validação

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

### Python
- pyproject.toml como único ponto de configuração
- src layout — evitar importações ambíguas
- Type hints obrigatórios em código de produção
- Ruff para lint/format, pytest para testes
- Lockfile reprodutível versionado no repositório

### Go
- go.mod e go.sum versionados
- cmd/ para entrypoints, internal/ como padrão
- context.Context como primeiro parâmetro em funções com I/O
- Erros com contexto usando %w
- Table-driven tests com -race em CI
