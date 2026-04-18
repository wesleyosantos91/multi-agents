# Multi-Agent Orchestration para Claude Code

## O que e isso?

Uma estrutura de **orquestracao multiagente** para o [Claude Code](https://docs.anthropic.com/en/docs/claude-code) que simula um **time de engenharia completo** dentro do seu terminal.

Em vez de um unico agente fazendo tudo, voce tem **24 agentes especializados** — cada um com papel, escopo, checklist e formato de saida definidos — coordenados por um **orquestrador principal** (o `staff-engineer-orchestrator`) que funciona como maestro.

Alem dos agentes, o projeto inclui **33 slash commands customizados**, **44 skills globais reutilizaveis**, **permissoes granulares**, **hooks de seguranca** e uma configuracao completa para workflow profissional.

### Analogia simples

Imagine que voce tem uma demanda tecnica complexa. Em vez de pedir para um unico engenheiro resolver tudo sozinho, voce:

1. Leva a demanda para o **staff engineer** (orquestrador)
2. Ele distribui a analise para os especialistas do time
3. Cada especialista analisa sob sua perspectiva
4. O staff engineer consolida tudo, resolve conflitos e entrega o plano final

Isso e exatamente o que essa estrutura faz — automaticamente, dentro do Claude Code.

---

## Por que usar?

### O problema

Quando voce usa um unico agente de IA para tarefas complexas:

- Ele tenta resolver tudo de uma vez, sem analise adequada
- Perde perspectivas importantes (seguranca, performance, operabilidade)
- Nao diferencia risco critico de melhoria futura
- Nao considera trade-offs sob multiplas perspectivas
- Tende a overengineering ou a solucoes incompletas

### A solucao

Com multiagentes, cada especialista foca no que sabe. O orquestrador garante que nenhuma perspectiva e ignorada e que a resposta final e consolidada e priorizada.

### Ganhos concretos

| Ganho | Descricao |
|-------|-----------|
| **Cobertura ampla** | 24 perspectivas especializadas em vez de uma generica |
| **Stack poliglota** | Suporte nativo a Java, Python, Go, Frontend, Mobile e AWS Serverless |
| **Slash commands** | 33 atalhos para acoes frequentes — `/review`, `/implement`, `/debug`, `/refactor`, etc. |
| **Seguranca integrada** | Hooks que bloqueiam edicao de arquivos sensiveis e alertam sobre segredos |
| **Qualidade de analise** | Cada agente tem checklist e regras mandatorias do seu dominio |
| **Rastreabilidade** | Saida estruturada com secoes fixas — facil de auditar e comparar |
| **Conflitos explicitos** | Quando dois agentes discordam, o orquestrador explicita e resolve |
| **Priorizacao** | Plano final ordenado por prioridade com justificativa |
| **Riscos visiveis** | Riscos remanescentes listados explicitamente |
| **Reproducibilidade** | Mesma estrutura de resposta toda vez, independente da demanda |
| **Escalabilidade do time** | Facil adicionar novos agentes sem quebrar o fluxo |

### Trade-offs

| Trade-off | Descricao |
|-----------|-----------|
| **Latencia** | Multiplos agentes = mais tempo de resposta. Para tarefas triviais, pode ser excessivo |
| **Custo de tokens** | Cada agente consome tokens. Demandas simples custam mais que o necessario |
| **Complexidade inicial** | Precisa entender a estrutura antes de usar com eficiencia |
| **Maturidade do Claude Code** | O recurso de agentes customizados ainda esta em evolucao |
| **Overhead para tarefas simples** | Para um bugfix pontual, acionar 24 agentes e desproporcional |

**Regra pratica**: use o orquestrador para demandas nao triviais. Para tarefas simples, use um slash command direto ou acione o agente relevante.

---

## Estrutura do repositorio

```
.
├── CLAUDE.md                                          # Governanca do projeto
├── README.md                                          # Este arquivo
└── .claude/
    ├── settings.json                                  # Permissoes, hooks e configuracao
    ├── settings.local.json                            # Overrides locais (nao commitar segredos)
    ├── commands/                                      # 33 slash commands customizados
    │   ├── review.md                                  # /review — revisao inteligente da branch
    │   ��── full-review.md                             # /full-review — revisao completa (todos agentes)
    │   ├── implement.md                               # /implement — analise + implementacao
    │   ├── pre-pr.md                                  # /pre-pr — checklist GO/NO-GO antes de PR
    │   ├── arch-review.md                             # /arch-review — arquitetura e boundaries
    │   ├── security-check.md                          # /security-check — seguranca e OWASP
    │   ├── compliance.md                              # /compliance — LGPD/GDPR
    │   ├── contract-review.md                         # /contract-review — contratos de borda
    │   ├── check-deps.md                              # /check-deps — versoes GA via WebSearch
    │   ├── data-review.md                             # /data-review — dados e persistencia
    │   ├─�� data-platform.md                           # /data-platform — pipelines de dados
    │   ├── qa-review.md                               # /qa-review — testes e qualidade
    │   ├── perf-review.md                             # /perf-review — performance e confiabilidade
    │   ├── sre-review.md                              # /sre-review — operabilidade e deploy
    │   ├── cicd-review.md                             # /cicd-review — pipelines CI/CD
    │   ├── finops.md                                  # /finops — custo AWS
    │   ├── incident-readiness.md                      # /incident-readiness — SLOs e runbooks
    │   ├── local-setup.md                             # /local-setup — ambiente de dev local
    │   ├── docs.md                                    # /docs — documentacao tecnica
    │   └── adr.md                                     # /adr — Architecture Decision Record
    └── agents/                                        # 24 agentes especializados
        ├── staff-engineer-orchestrator.md             # Maestro principal (opus)
        ├── dependency-versions-reviewer.md            # Versoes GA de dependencias (WebSearch)
        ├── tech-lead-reviewer.md                      # Pragmatismo e manutenibilidade
        ├── architect-reviewer.md                      # Arquitetura e boundaries
        ├── api-contract-reviewer.md                   # Contratos de borda e schema governance
        ├── security-reviewer.md                       # Seguranca e hardening (WebSearch para CVEs)
        ├── compliance-reviewer.md                     # LGPD, GDPR, compliance serverless
        ├── ad-dba-reviewer.md                         # Dados e persistencia
        ├── data-engineering-aws-architect.md          # Pipelines de dados, Glue, EMR (opus)
        ├── java-specialist.md                         # Java 25, Spring Boot, Quarkus, Micronaut
        ├── jakarta-ee-specialist.md                   # Jakarta EE 11, MicroProfile 7.0, WildFly, Open Liberty
        ├── python-specialist.md                       # Python, pyproject.toml, pytest, Ruff
        ├── go-specialist.md                           # Go, go.mod, interfaces, testing
        ├── frontend-specialist.md                     # React, Angular, AngularJS (migracao)
        ├── mobile-native-specialist.md                # Android (Kotlin+Compose), iOS (Swift+SwiftUI)
        ├── software-engineer.md                       # Implementacao minima correta
        ├── sre-platform-engineer.md                   # Operabilidade, deploy, IaC
        ├── cicd-pipeline-engineer.md                  # GitHub Actions, deploy Lambda, rollback
        ├── incident-response-reviewer.md              # SLOs/SLIs, runbooks, chaos engineering
        ���── finops-reviewer.md                         # Custo AWS, rightsizing (WebSearch para pricing)
        ├── devex-reviewer.md                          # Onboarding, ambiente local (Bash para validar)
        ├── qa-quality-engineer.md                     # Testes e qualidade (Bash para rodar testes)
        ├── performance-reliability-reviewer.md        # Performance e confiabilidade
        └── tech-writer.md                             # Documentacao tecnica
```

---

## Slash Commands — Referencia rapida

### Orquestracao

| Comando | Agente(s) | Proposito |
|---------|-----------|-----------|
| `/review` | staff-engineer-orchestrator | Revisao inteligente com triage automatico |
| `/full-review` | staff-engineer-orchestrator (N4) | Revisao completa — todos os agentes relevantes |
| `/implement` | staff-engineer-orchestrator | Analise + implementacao de demanda |
| `/pre-pr` | staff-engineer-orchestrator | Checklist GO/NO-GO antes de abrir PR |

### Revisoes especializadas

| Comando | Agente(s) | Proposito |
|---------|-----------|-----------|
| `/arch-review` | architect-reviewer | Arquitetura, boundaries, trade-offs |
| `/security-check` | security-reviewer | Seguranca, OWASP, hardening |
| `/compliance` | compliance-reviewer | LGPD/GDPR, residencia de dados |
| `/contract-review` | api-contract-reviewer | Contratos, breaking changes, schema |
| `/check-deps` | dependency-versions-reviewer | Versoes GA via WebSearch |
| `/data-review` | ad-dba-reviewer | Dados, persistencia, modelagem |
| `/data-platform` | data-engineering-aws-architect | Pipelines de dados, ETL, data lake |
| `/qa-review` | qa-quality-engineer | Testes, edge cases, regressoes |
| `/perf-review` | performance-reliability-reviewer | Throughput, latencia, escalabilidade |
| `/sre-review` | sre-platform-engineer | Operabilidade, deploy, observabilidade |
| `/cicd-review` | cicd-pipeline-engineer | Pipelines CI/CD, deploy strategy |
| `/finops` | finops-reviewer | Custo AWS, billing anti-patterns |
| `/incident-readiness` | incident-response-reviewer | SLOs, runbooks, chaos engineering |
| `/local-setup` | devex-reviewer | Ambiente local, onboarding |
| `/docs` | tech-writer | Documentacao tecnica |
| `/adr` | tech-writer | Architecture Decision Records |

### Workflows de desenvolvimento

| Comando | Tipo | Proposito |
|---------|------|-----------|
| `/debug` | Workflow | Investigacao sistematica de causa raiz com reproducao, diagnostico e validacao |
| `/refactor` | Workflow | Refatoracao segura com mapeamento de dependentes e validacao de regressao |
| `/scaffold` | Workflow | Criar novo modulo/componente seguindo padroes existentes do projeto |
| `/test-gen` | Workflow | Gerar ou melhorar testes — identifica gaps e gera cobertura por comportamento |
| `/explain` | Workflow | Explicar codigo, arquitetura ou fluxo de forma clara e objetiva |
| `/quick-fix` | Workflow | Correcao pontual e trivial sem acionar o orquestrador |
| `/hotfix` | Workflow | Correcao emergencial com blast radius minimo e rollback documentado |
| `/optimize` | Workflow | Identificar gargalo e otimizar performance com trade-offs explicitos |

### Operacional

| Comando | Tipo | Proposito |
|---------|------|-----------|
| `/health-check` | Diagnostico | Diagnostico rapido de saude: build, testes, deps, codigo, infra |
| `/tech-debt` | Diagnostico | Inventario priorizado de debito tecnico (P0-P3) |
| `/migrate` | Workflow | Planejamento e execucao segura de migracao tecnica |
| `/changelog` | Geracao | Gerar changelog estruturado da branch vs main |
| `/runbook` | Geracao | Criar runbook operacional com alarmes, procedimentos e escalacao |

Todos os commands aceitam argumentos. Exemplo: `/debug o endpoint /orders retorna 500 quando o payload tem campo opcional nulo`

---

## Permissoes e Seguranca

### Permissoes (`.claude/settings.json`)

O projeto configura permissoes granulares para evitar prompts repetitivos:

**Allow (automatico)**:
- Ferramentas de build: `git`, `make`, `docker`, `mvn`, `gradle`, `go`, `python`, `npm`, `terraform`, `aws`, `gh`
- Comandos utilitarios: `ls`, `mkdir`, `cp`, `mv`, `find`, `curl`, `jq`, `which`
- WebSearch global (essencial para `dependency-versions-reviewer`)
- WebFetch para 16 dominios confiaveies (Maven Central, PyPI, npm, Go pkg, Terraform Registry, Docker Hub, docs AWS, Spring, Quarkus, Micronaut, Jakarta EE, MicroProfile)

**Deny (bloqueado)**:
- `rm -rf /` e `rm -rf /*`
- `git push --force`
- `git reset --hard`

### Hooks de seguranca

| Hook | Trigger | Acao |
|------|---------|------|
| PreToolUse (Edit/Write) | Antes de editar/criar arquivo | **Bloqueia** edicao de arquivos sensiveis (`.env`, `.pem`, `.key`, `.secret`, `.credentials`, `.token`) |
| PostToolUse (Bash) | Apos executar comando | **Alerta** se output contem possiveis segredos (AWS keys, private keys, passwords) |

---

## Ferramentas por agente

| Ferramenta | O que faz | Quem usa |
|------------|-----------|----------|
| `Read` | Le arquivos | Todos (24 agentes) |
| `Glob` | Busca arquivos por padrao | Todos (24 agentes) |
| `Grep` | Busca conteudo em arquivos | Todos (24 agentes) |
| `Edit` | Edita arquivos existentes | orchestrator, software-engineer, tech-writer |
| `Write` | Cria arquivos novos | orchestrator, software-engineer, tech-writer |
| `Bash` | Executa comandos no terminal | orchestrator, software-engineer, sre-platform, tech-writer, qa-quality-engineer, devex-reviewer |
| `Agent` | Invoca outros agentes | orchestrator (apenas ele) |
| `WebSearch` | Busca informacoes na web | dependency-versions, data-engineering, security-reviewer, finops-reviewer |
| `WebFetch` | Acessa URLs especificas | dependency-versions, data-engineering, security-reviewer, finops-reviewer |

### Decisao de design

- **Revisores puros** (tech-lead, architect, api-contract, compliance, ad-dba, performance, incident-response, cicd-pipeline, language specialists) → somente leitura. Evita mudancas sem consolidacao.
- **Revisores com capacidade de execucao** (qa-quality-engineer, devex-reviewer) → leitura + Bash. Precisam executar para validar (rodar testes, testar setup commands).
- **Revisores com acesso web** (security-reviewer, finops-reviewer) → leitura + WebSearch/WebFetch. Precisam de dados em tempo real (CVEs, pricing AWS).
- **Engenheiros** (software-engineer, tech-writer) → leitura + escrita + Bash. Implementam mudancas.
- **Orquestrador** → todas as ferramentas. Coordena e pode agir diretamente em tarefas triviais.

### Escolha de modelo

| Modelo | Quando usar | Agentes |
|--------|-------------|---------|
| `opus` | Raciocinio complexo, consolidacao, decisoes arquiteturais | orchestrator, data-engineering-aws-architect |
| `sonnet` | Analise focada, revisao, implementacao | Todos os demais (22 agentes) |

---

## Ordem de consulta dos agentes

O orquestrador segue esta ordem preferencial:

| # | Agente | Foco |
|---|--------|------|
| 0 | `dependency-versions-reviewer` | **Obrigatorio** quando ha dependencias — versoes GA via WebSearch |
| 1 | `tech-lead-reviewer` | Pragmatismo, simplicidade, custo de manutencao |
| 2 | `architect-reviewer` | Boundaries, acoplamento, resiliencia, modelo de execucao |
| 3 | `api-contract-reviewer` | Contratos de borda, breaking changes, schema governance |
| 4 | `security-reviewer` | Seguranca, hardening, CVEs via WebSearch |
| 5 | `compliance-reviewer` | LGPD, GDPR, residencia de dados, serverless compliance |
| 6 | `ad-dba-reviewer` | Dados, modelagem, queries, indices, CAP theorem |
| 7 | `data-engineering-aws-architect` | *(quando pipelines de dados)* Glue, EMR, Kinesis, Athena |
| 8 | `java-specialist` | *(quando stack Java)* Java 25, Spring Boot, Quarkus, Micronaut |
| 8 | `jakarta-ee-specialist` | *(quando Jakarta EE)* CDI, JAX-RS, JPA, MicroProfile |
| 8 | `python-specialist` | *(quando stack Python)* pyproject.toml, pytest, Ruff |
| 8 | `go-specialist` | *(quando stack Go)* go.mod, interfaces, context |
| 8 | `frontend-specialist` | *(quando frontend)* React, Angular, AngularJS |
| 8 | `mobile-native-specialist` | *(quando mobile)* Android Kotlin+Compose, iOS Swift+SwiftUI |
| 9 | `software-engineer` | Implementacao minima correta (apos versoes validadas) |
| 10 | `sre-platform-engineer` | Operabilidade, deploy, observabilidade, IaC |
| 11 | `cicd-pipeline-engineer` | *(quando CI/CD)* GitHub Actions, deploy Lambda, rollback |
| 12 | `incident-response-reviewer` | *(quando producao)* SLOs/SLIs, runbooks, chaos engineering |
| 13 | `finops-reviewer` | Custo AWS, rightsizing, pricing via WebSearch |
| 14 | `devex-reviewer` | Onboarding, ambiente local, validacao de setup via Bash |
| 15 | `qa-quality-engineer` | Testes, qualidade, execucao de testes via Bash |
| 16 | `performance-reliability-reviewer` | Throughput, latencia, escalabilidade, cold start |
| 17 | `tech-writer` | *(quando documentacao)* README, ADRs, troubleshooting |

---

## Skills Globais (`~/.claude/skills/`)

Alem dos agentes e slash commands (que sao especificos deste projeto), o repositorio inclui **44 skills globais** instaladas em `~/.claude/skills/`. Skills sao diferentes de commands:

| Aspecto | Commands (`.claude/commands/`) | Skills (`~/.claude/skills/`) |
|---------|-------------------------------|------------------------------|
| Escopo | Projeto atual | **Todos os projetos** |
| Ativacao | `/nome` explicito | **On-demand automatico** quando relevante |
| Custo de tokens | Carrega ao invocar | **Zero ate ser usado** |
| Conteudo | Workflows que acionam agentes | Conhecimento procedural reutilizavel |

### Skills disponiveis

#### Java
| Skill | Conteudo |
|-------|----------|
| `java-project-setup` | Estrutura, records, virtual threads, Spring Boot config, ArchUnit |
| `java-spring-patterns` | Resilience4j, Security JWT, Kafka/SQS, caching, scheduling |
| `java-testing` | JUnit 5, Testcontainers, MockMvc, ArchUnit, PIT mutacao |
| `java-quarkus-patterns` | Quarkus dev mode, CDI, RESTEasy, Panache, native build, Lambda |
| `java-micronaut-patterns` | Micronaut DI compile-time, HTTP client, GraalVM, Lambda |
| `jakarta-ee-patterns` | CDI, JAX-RS, JPA, JMS, MicroProfile FT/Config/Health |

#### Go
| Skill | Conteudo |
|-------|----------|
| `go-project-setup` | cmd/internal layout, interfaces, slog, functional options |
| `go-web-frameworks` | Gin, Chi, Echo: routing, middleware, validation, graceful shutdown |
| `go-testing` | Table-driven, Testcontainers, httptest, benchmarks, race detection |

#### Python
| Skill | Conteudo |
|-------|----------|
| `python-project-setup` | src layout, pyproject.toml, FastAPI, structlog, Ruff |
| `python-fastapi-patterns` | Pydantic v2, async, DI, middleware, OpenAPI, SQLAlchemy async |
| `python-testing` | pytest fixtures, parametrize, AsyncMock, Testcontainers |

#### Frontend
| Skill | Conteudo |
|-------|----------|
| `react-patterns` | Hooks, React Query, Zustand, Testing Library, MSW, Vite |
| `angular-patterns` | Standalone Components, Signals, inject(), HttpClient, RxJS |
| `angularjs-migration` | ngUpgrade, dual-boot, strangler fig, migracao incremental |

#### Mobile
| Skill | Conteudo |
|-------|----------|
| `android-patterns` | Kotlin, Jetpack Compose, MVVM, Hilt, Room, Coroutines |
| `ios-patterns` | Swift, SwiftUI, @Observable, async/await, SwiftData, Navigation |

#### AWS
| Skill | Conteudo |
|-------|----------|
| `aws-architecture-patterns` | API GW+Lambda, SQS+Lambda, EventBridge, Step Functions, DynamoDB |
| `aws-iac-patterns` | Terraform multi-env, remote state, modulos, IAM, alarmes |
| `aws-lambda-checklist` | Handler, IAM, cold start, deploy, DLQ, observabilidade |
| `aws-observability` | CloudWatch, X-Ray, Log Insights, dashboards, alerting |

#### Data Engineering
| Skill | Conteudo |
|-------|----------|
| `spark-data-engineering` | PySpark, batch, streaming, Glue, EMR, data quality |

#### Contratos e Comunicacao
| Skill | Conteudo |
|-------|----------|
| `grpc-patterns` | Protobuf, service definition, streaming, deadlines, interceptors |
| `graphql-patterns` | Schema design, resolvers, N+1, DataLoader, pagination |
| `async-messaging-patterns` | SQS, Kafka, EventBridge, idempotencia, DLQ, ordering |

#### QA e Processo
| Skill | Conteudo |
|-------|----------|
| `qa-process` | Piramide de testes, criterios de aceite, edge cases, quality gates |
| `software-engineering-process` | Design, code review, CI/CD, deploy, SLOs |
| `testing-strategies` | Estrategia por tipo de codigo, exemplos por linguagem |
| `performance-testing` | k6, Gatling, JMH, load testing, benchmarks, profiling |

#### Arquitetura e Documentacao
| Skill | Conteudo |
|-------|----------|
| `c4-model` | Context, Container, Component, Code + Structurizr, Mermaid |
| `adr-template` | ADR: template, quando criar, exemplos, boas praticas |
| `twelve-factor-app` | 12 fatores, cloud-native, config, stateless, logs |

#### Transversal
| Skill | Conteudo |
|-------|----------|
| `code-review` | Revisao estruturada: correcao, seguranca, qualidade, testes |
| `commit-message` | Conventional Commits com exemplos |
| `pr-description` | Template de PR: summary, changes, test plan |
| `security-audit` | Auditoria: segredos, injection, auth, dados, deps |
| `api-design` | REST best practices: URLs, methods, status codes, paginacao, erros |
| `error-handling` | Tratamento de erros por linguagem, RFC 9457 |
| `dockerfile-best-practices` | Multi-stage, seguranca, cache, templates por linguagem |
| `git-workflow` | Merge conflicts, rebase, cherry-pick, bisect, recovery |
| `terraform-module` | Estrutura, variables, outputs, naming, state, seguranca |
| `observability-setup` | Logs, metricas RED/USE, tracing, OpenTelemetry |
| `database-migration` | Zero-downtime, expand-contract, backfill, rollback |
| `dependency-upgrade` | Processo seguro de upgrade por ecossistema |

### Como instalar

As skills ficam em `~/.claude/skills/`. Para usar em qualquer projeto:

1. Copie a pasta `skills/` para `~/.claude/skills/`
2. Copie o `SKILL.md` (indice) para `~/.claude/skills/SKILL.md`
3. Pronto — o Claude Code carrega automaticamente quando relevante

---

## Como funciona na pratica

### Fluxo padrao (demanda nao trivial)

```
Voce faz uma pergunta ou pede uma implementacao
         |
         v
+---------------------------------+
|  staff-engineer-orchestrator    |  <- Entende a demanda, identifica stack e modulos
+----------------+----------------+
                 |
                 v
    Aciona especialistas (em paralelo quando possivel)
                 |
  +----+----+----+----+----+----+----+----+----+----+----+
  v    v    v    v    v    v    v    v    v    v    v    v
dep- tech- archi- api- sec- compl- dba java/ soft- sre  qa  ...
vers lead  tect  cont rity iance      py/go  ware plat
  |    |    |    |    |    |    |    |    |    |    |
  +----+----+----+----+----+----+----+----+----+----+
                 |
                 v
+---------------------------------+
|  staff-engineer-orchestrator    |  <- Consolida, resolve conflitos, prioriza
+----------------+----------------+
                 |
                 v
    Resposta final estruturada (ate 26 secoes)
```

### Exemplos de uso

#### Exemplo 1: Usando slash commands (forma rapida)

```bash
# Revisao inteligente da branch
/review

# Checklist antes de abrir PR
/pre-pr

# Implementar feature
/implement Adicionar endpoint REST para consulta de pedidos com paginacao

# Investigar bug
/debug o endpoint /orders retorna 500 quando o payload tem campo opcional nulo

# Gerar testes
/test-gen src/main/java/com/example/domain/OrderService.java

# Refatorar com seguranca
/refactor extrair validacao de pedido do controller para o domain service

# Criar novo modulo seguindo padroes
/scaffold lambda Python para processar eventos de pagamento via SQS

# Correcao rapida sem orquestracao
/quick-fix corrigir typo no campo "stauts" para "status" na entity Order

# Diagnostico de saude do projeto
/health-check lambda-java-spring

# Verificar dependencias
/check-deps pom.xml

# Gerar changelog
/changelog
```

#### Exemplo 2: Nova feature em Java (Spring Boot)

```
Voce: Preciso adicionar um endpoint REST para consulta de pedidos
      com paginacao, filtro por status e ordenacao por data.

Orchestrator:
  -> Aciona dependency-versions-reviewer (versao Spring Boot atual)
  -> Aciona tech-lead + architect + api-contract + security + java-specialist (em paralelo)
  -> Aciona software-engineer (implementacao)
  -> Aciona qa-quality-engineer (testes JUnit 5, Testcontainers)
  -> Consolida tudo em resposta estruturada
```

#### Exemplo 3: Worker Python para processar eventos SQS

```
Voce: Preciso de um worker Python que consome eventos SQS,
      valida payload e persiste no DynamoDB. Lambda ou ECS?

Orchestrator:
  -> Aciona dependency-versions-reviewer (boto3, runtimes AWS)
  -> Aciona architect-reviewer (Lambda vs ECS, modelo de execucao)
  -> Aciona security + compliance + ad-dba + python-specialist (em paralelo)
  -> Aciona software-engineer + sre-platform (implementacao e operacao)
  -> Aciona finops-reviewer (Lambda vs ECS custo)
  -> Consolida com decisao justificada
```

#### Exemplo 4: Tarefa simples (sem orquestracao)

```
Voce: /quick-fix corrigir typo no campo "stauts" para "status" na entity Order

  -> Sem orquestracao — le o codigo, corrige, roda testes
  -> Resposta em 1-3 linhas
```

#### Exemplo 5: Acionar agente especifico

```
Voce: Usando o security-reviewer, revise a configuracao de autenticacao
      do endpoint /api/v1/payments.

  -> Somente o security-reviewer analisa
  -> Resposta focada em seguranca
```

---

## Como os agentes sao definidos

Cada agente e um arquivo Markdown em `.claude/agents/` com duas partes:

### 1. Frontmatter YAML (metadados)

```yaml
---
name: nome-do-agente
description: "Descricao curta do papel do agente."
tools:
  - Read
  - Glob
  - Grep
model: sonnet
---
```

| Campo | Descricao |
|-------|-----------|
| `name` | Identificador unico do agente. Usado para referencia e invocacao. |
| `description` | **Campo critico.** O Claude Code usa esse campo para decidir automaticamente quando invocar o agente. Uma descricao clara com condicoes de uso ("use para X, Y, Z") melhora a selecao automatica. |
| `tools` | Lista de ferramentas que o agente pode usar. Controla o que ele pode fazer. |
| `model` | Modelo Claude a ser usado (`opus`, `sonnet`, `haiku`). |

### 2. Corpo Markdown (instrucoes)

Apos o frontmatter, o conteudo Markdown define:

- **Papel** — o que o agente faz
- **Escopo** — o que ele deve revisar ou implementar
- **Stack e contexto** — tecnologias que ele conhece
- **Regras mandatorias** — restricoes que ele deve seguir
- **Checklist** — itens que ele deve verificar
- **Modo rapido** — formato compacto para respostas breves
- **Formato de saida** — secoes obrigatorias na resposta

---

## Como criar um novo agente

### Passo 1: Crie o arquivo

```bash
touch .claude/agents/meu-novo-agente.md
```

### Passo 2: Defina o frontmatter

```yaml
---
name: meu-novo-agente
description: "Descricao curta e objetiva do papel."
tools:
  - Read
  - Glob
  - Grep
model: sonnet
---
```

### Passo 3: Escreva as instrucoes

```markdown
# Meu Novo Agente

Voce e o [papel] de um sistema critico, com stack poliglota (Java, Python, Go)
e suporte a AWS Serverless. Seu papel e [descricao clara].

## Escopo de revisao
- Item 1
- Item 2

## Regras mandatorias
- Regra 1
- Regra 2

## Checklist de revisao
- [ ] Check 1?
- [ ] Check 2?

## Modo rapido
Quando acionado com escopo restrito, responda com:
- **Veredicto**: uma linha
- Maximo 3 bullets
- Acao prioritaria em 1 frase

## Formato de saida obrigatorio
### 1. Secao 1
### 2. Secao 2
```

### Passo 4: Crie um slash command (opcional)

```bash
touch .claude/commands/meu-command.md
```

### Passo 5: Registre no orquestrador e CLAUDE.md

1. Adicione na ordem de consulta em `.claude/agents/staff-engineer-orchestrator.md`
2. Adicione na lista de agentes em `CLAUDE.md`

---

## Como criar um novo slash command

Cada command e um arquivo Markdown em `.claude/commands/`:

```markdown
Acione o `nome-do-agente` para [objetivo].

## Escopo
- Se `$ARGUMENTS` estiver vazio, [comportamento padrao]
- Se `$ARGUMENTS` contiver algo, [comportamento especifico]

## O que avaliar
- Item 1
- Item 2

## Entrada do usuario
$ARGUMENTS
```

A variavel `$ARGUMENTS` captura tudo que o usuario digita apos o comando.

---

## Anatomia da resposta do orquestrador

O `staff-engineer-orchestrator` usa **dois formatos** conforme o nivel da demanda:

### Formato compacto (Nivel 2 e 3)

Para demandas pontuais e moderadas — mais agil:

```
1. Diagnostico
2. Achados por especialista (apenas os acionados)
3. Conflitos (se houver)
4. Plano
5. Diff sugerido
6. Riscos remanescentes
7. Validacao
```

### Formato completo (Nivel 4)

Para demandas amplas — 26 secoes cobrindo todos os especialistas:

```
 1. Diagnostico inicial
 2. Stack e modulos impactados
 3-20. Achados de cada agente (omite os nao aplicaveis)
21. Conflitos entre recomendacoes
22. Plano final priorizado
23. Diff sugerido
24. Riscos remanescentes
25. Estrategia de validacao
26. Documentacao a atualizar
```

---

## Papel do CLAUDE.md

O `CLAUDE.md` e o documento de governanca do projeto. O Claude Code le esse arquivo automaticamente ao abrir o repositorio.

| Secao | O que faz |
|-------|-----------|
| Agente principal | Define `staff-engineer-orchestrator` como coordenador |
| Stack oficial | Java, Python, Go, Frontend, Mobile, AWS Serverless |
| Regras de bordas | `web/` (sincrona) e `message/` (assincrona) |
| Organizacao arquitetural | Onde cada coisa fica |
| Checklist transversal | O que toda proposta deve validar |
| Ordem de consulta | Sequencia dos 24 agentes |
| Regras de execucao | Comportamentos obrigatorios |
| Regras por framework | Idiomatismo de cada tecnologia |

**Todos os agentes respeitam o CLAUDE.md.** Se voce mudar uma regra la, todos os agentes passam a segui-la.

---

## Customizacao

### Mudar o modelo de um agente

```yaml
model: opus    # mais capaz, mais lento, mais caro
model: sonnet  # equilibrado (padrao dos especialistas)
model: haiku   # mais rapido, mais barato, menos capaz
```

### Adicionar ferramentas a um agente

```yaml
tools:
  - Read
  - Glob
  - Grep
  - Edit      # editar arquivos
  - Bash      # executar comandos
  - WebSearch # buscar na web
```

### Remover um agente do fluxo

1. Remova da lista de consulta no `staff-engineer-orchestrator.md`
2. Remova da lista no `CLAUDE.md`
3. Opcionalmente, delete o arquivo `.claude/agents/nome.md`

---

## Perguntas frequentes

### Preciso acionar todos os agentes sempre?

Nao. O orquestrador classifica cada demanda em 4 niveis e aciona apenas os agentes relevantes:

| Nivel | Descricao | Agentes |
|-------|-----------|---------|
| 1 — Trivial | Typo, rename, config obvia | Nenhum (age direto) |
| 2 — Pontual | Bug isolado, ajuste de teste | 2-3 agentes |
| 3 — Moderado | Nova feature, mudanca de contrato | 5-8 agentes |
| 4 — Amplo | Novo servico, mudanca arquitetural | Pipeline completa |

### Posso usar sem o orquestrador?

Sim. Use slash commands diretos (`/security-check`, `/check-deps`, etc.) ou acione qualquer agente por nome.

### Funciona com qual stack?

| Camada | Tecnologias suportadas |
|--------|----------------------|
| Backend | Java 25 (Spring Boot, Quarkus, Micronaut), Python, Go |
| Jakarta EE | Jakarta EE 11, MicroProfile 7.0, WildFly, Open Liberty, Payara, TomEE |
| Frontend | React (Vite+TS), Angular (Standalone+Signals), AngularJS (migracao) |
| Mobile | Android (Kotlin+Compose), iOS (Swift+SwiftUI) |
| Cloud | AWS (Lambda, API GW, EventBridge, SQS, SNS, Step Functions, DynamoDB, S3, ECS) |
| Data | Glue, EMR, Kinesis, MSK, Athena, Redshift, Lake Formation |
| IaC | Terraform |
| Local | Docker, Ministack (porta 4566) |

### Posso usar em outro repositorio?

Sim. Copie a pasta `.claude/` e o `CLAUDE.md` para outro repo e adapte o conteudo. A estrutura e agnostica — usa `<project-root>/` e `<base-package>/` como placeholders.

---

## Referencias

- [Claude Code — Documentacao oficial](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code — Custom Agents](https://docs.anthropic.com/en/docs/claude-code/agents)
- [Claude Code — Slash Commands](https://docs.anthropic.com/en/docs/claude-code/slash-commands)
- [Claude Code — CLAUDE.md](https://docs.anthropic.com/en/docs/claude-code/memory)
- [Claude Code — Hooks](https://docs.anthropic.com/en/docs/claude-code/hooks)
