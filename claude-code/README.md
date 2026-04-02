# Multi-Agent Orchestration para Claude Code

## O que e isso?

Uma estrutura de **orquestracao multiagente** para o [Claude Code](https://docs.anthropic.com/en/docs/claude-code) que simula um **time de engenharia completo** dentro do seu terminal.

Em vez de um unico agente fazendo tudo, voce tem **18 agentes especializados** — cada um com papel, escopo, checklist e formato de saida definidos — coordenados por um **orquestrador principal** (o `staff-engineer-orchestrator`) que funciona como maestro.

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
| **Cobertura ampla** | 18 perspectivas especializadas em vez de uma generica |
| **Stack poliglota** | Suporte nativo a Java, Python, Go e AWS Serverless — cada linguagem tem especialista proprio |
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
| **Overhead para tarefas simples** | Para um bugfix pontual, acionar 18 agentes e desproporcional |

**Regra pratica**: use o orquestrador para demandas nao triviais. Para tarefas simples, acione diretamente o agente relevante.

---

## Estrutura do repositorio

```
.
├── CLAUDE.md                                          # Governanca do projeto
├── README.md                                          # Este arquivo
└── .claude/
    ├── settings.json                                  # Configuracao do Claude Code
    └── agents/                                        # Agentes especializados
        ├── staff-engineer-orchestrator.md             # Maestro principal
        ├── dependency-versions-reviewer.md            # Versoes GA de dependencias (WebSearch)
        ├── tech-lead-reviewer.md                      # Pragmatismo e manutenibilidade
        ├── architect-reviewer.md                      # Arquitetura e boundaries
        ├── api-contract-reviewer.md                   # Contratos de borda e schema governance
        ├── security-reviewer.md                       # Seguranca e hardening
        ├── compliance-reviewer.md                     # LGPD, GDPR, compliance serverless
        ├── ad-dba-reviewer.md                         # Dados e persistencia
        ├── data-engineering-aws-architect.md          # Pipelines de dados, Glue, EMR, Kinesis
        ├── java-specialist.md                         # Java 25, Spring Boot, Quarkus, Micronaut
        ├── python-specialist.md                       # Python, pyproject.toml, pytest, Ruff
        ├── go-specialist.md                           # Go, go.mod, interfaces, testing
        ├── software-engineer.md                       # Implementacao minima correta
        ├── sre-platform-engineer.md                   # Operabilidade, deploy, IaC
        ├── finops-reviewer.md                         # Custo AWS, rightsizing, billing
        ├── devex-reviewer.md                          # Onboarding, ambiente local, Dev Container
        ├── qa-quality-engineer.md                     # Testes e qualidade
        ├── performance-reliability-reviewer.md        # Performance e confiabilidade
        └── tech-writer.md                             # Documentacao tecnica
```

### O que cada arquivo faz

| Arquivo | Funcao |
|---------|--------|
| `CLAUDE.md` | Documento de governanca lido automaticamente pelo Claude Code. Define stack, regras arquiteturais, checklists transversais e ordem de consulta dos agentes. **E aqui que o `staff-engineer-orchestrator` e definido como agente padrao** — a instrucao "toda demanda nao trivial deve passar pelo orquestrador" e lida e seguida pelo Claude automaticamente. |
| `.claude/settings.json` | Configuracoes do Claude Code para o projeto: permissoes de ferramentas, hooks, variaveis de ambiente. Nao define o agente padrao — isso e responsabilidade do `CLAUDE.md`. |
| `.claude/agents/*.md` | Cada arquivo define um agente com: papel, escopo, regras, checklist e formato de saida obrigatorio. O campo `description` de cada arquivo e o **gatilho** que o Claude usa para selecionar automaticamente qual agente invocar. |

---

## Como funciona na pratica

### Fluxo padrao (demanda nao trivial)

```
Voce faz uma pergunta ou pede uma implementacao
         │
         ▼
┌──────────────────────────────────┐
│  staff-engineer-orchestrator     │  ← Entende a demanda, identifica stack e modulos
└───────────────┬──────────────────┘
                │
                ▼
    Aciona especialistas (em paralelo quando possivel)
                │
  ┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐
  ▼    ▼    ▼    ▼    ▼    ▼    ▼    ▼    ▼    ▼    ▼
dep- tech- archi- api- sec- compl- dba  java/ soft- sre  qa ...
vers lead  tect  cont rity iance      py/go ware plat
  │    │    │    │    │    │    │    │    │    │    │
  └────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘
                │
                ▼
┌──────────────────────────────────┐
│  staff-engineer-orchestrator     │  ← Consolida, resolve conflitos, prioriza
└───────────────┬──────────────────┘
                │
                ▼
    Resposta final estruturada (26 secoes)
```

### Ordem de consulta

O orquestrador segue esta ordem preferencial:

| # | Agente | Foco |
|---|--------|------|
| 0 | `dependency-versions-reviewer` | Versoes GA via WebSearch — Java, Python, Go, AWS runtimes |
| 1 | `tech-lead-reviewer` | Pragmatismo, simplicidade, custo de manutencao |
| 2 | `architect-reviewer` | Boundaries, acoplamento, resiliencia, contratos |
| 3 | `api-contract-reviewer` | Contratos de borda, breaking changes, schema governance |
| 4 | `security-reviewer` | Seguranca, hardening, superficies de abuso |
| 5 | `compliance-reviewer` | LGPD, GDPR, residencia de dados, serverless compliance |
| 6 | `ad-dba-reviewer` | Dados, modelagem, queries, indices, CAP theorem |
| 7 | `data-engineering-aws-architect` | Pipelines de dados, Glue, EMR, Kinesis, Athena — trade-offs tecnico e financeiro |
| 8 | `java-specialist` | *(quando stack Java)* Java 25, Spring Boot, Quarkus, Micronaut |
| 8 | `python-specialist` | *(quando stack Python)* pyproject.toml, pytest, Ruff, Lambda Python |
| 8 | `go-specialist` | *(quando stack Go)* go.mod, interfaces, context, table-driven tests |
| 9 | `software-engineer` | Implementacao minima correta (apos versoes validadas) |
| 10 | `sre-platform-engineer` | Operabilidade, deploy, observabilidade, IaC |
| 11 | `finops-reviewer` | Custo AWS, rightsizing, anti-padroes de billing |
| 12 | `devex-reviewer` | Onboarding, ambiente local, docker-compose, Dev Container |
| 13 | `qa-quality-engineer` | Testes, qualidade, edge cases (Java, Python, Go, serverless) |
| 14 | `performance-reliability-reviewer` | Throughput, latencia, escalabilidade, cold start |
| 15 | `tech-writer` | Documentacao tecnica: README, getting-started, testing, troubleshooting |

---

## Como usar

### Pre-requisitos

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) instalado
- Repositorio clonado localmente

### Uso basico

```bash
# 1. Clone o repositorio
git clone <repo-url>
cd multi-agents/claude-code

# 2. Abra o Claude Code
claude

# 3. O staff-engineer-orchestrator ja e o agente padrao.
#    Basta fazer sua pergunta ou pedir uma implementacao.
```

### Exemplos de uso

#### Exemplo 1: Nova feature em Java (Spring Boot)

```
Voce: Preciso adicionar um endpoint REST para consulta de pedidos
      com paginacao, filtro por status e ordenacao por data.

Orchestrator:
  → Aciona dependency-versions-reviewer (versao Spring Boot atual)
  → Aciona tech-lead-reviewer (simplicidade, padroes)
  → Aciona architect-reviewer (boundaries, contratos REST)
  → Aciona api-contract-reviewer (OpenAPI, breaking changes)
  → Aciona security-reviewer (validacao, autorizacao)
  → Aciona ad-dba-reviewer (query, indice, paginacao)
  → Aciona java-specialist (idiomatismo Java 25, Spring MVC)
  → Aciona software-engineer (implementacao)
  → Aciona sre-platform-engineer (metricas, observabilidade)
  → Aciona qa-quality-engineer (testes JUnit 5, Testcontainers)
  → Aciona performance-reliability-reviewer (latencia, N+1)

  → Consolida tudo em resposta estruturada com 26 secoes
```

#### Exemplo 2: Worker Python para processar eventos SQS

```
Voce: Preciso de um worker Python que consome eventos SQS,
      valida payload e persiste no DynamoDB. Lambda ou ECS?

Orchestrator:
  → Aciona dependency-versions-reviewer (versao boto3, runtimes AWS)
  → Aciona architect-reviewer (Lambda vs ECS, model de execucao)
  → Aciona security-reviewer (IAM roles, dados sensiveis)
  → Aciona compliance-reviewer (LGPD, dados pessoais no payload)
  → Aciona ad-dba-reviewer (modelagem DynamoDB, partition key)
  → Aciona python-specialist (pyproject.toml, estrutura, pytest)
  → Aciona software-engineer (implementacao)
  → Aciona sre-platform-engineer (DLQ, CloudWatch, X-Ray)
  → Aciona finops-reviewer (Lambda vs ECS cost, DynamoDB capacity)
  → Aciona performance-reliability-reviewer (cold start, SQS visibility timeout)

  → Consolida com decisao justificada e plano de implementacao
```

#### Exemplo 3: API Go com consumer Kafka

```
Voce: Revise o consumer Kafka em Go que processa eventos de pagamento.
      Quero saber se esta resiliente e seguro para producao.

Orchestrator:
  → Aciona tech-lead-reviewer (complexidade, manutencao)
  → Aciona architect-reviewer (bordas assincronas, idempotencia)
  → Aciona security-reviewer (dados sensiveis em logs, payload)
  → Aciona go-specialist (goroutines, context, interfaces idiomaticas)
  → Aciona sre-platform-engineer (DLQ, metricas, lag)
  → Aciona qa-quality-engineer (testes -race, table-driven)
  → Aciona performance-reliability-reviewer (goroutine leaks, backpressure)

  → Consolida com riscos priorizados e plano de acao
```

#### Exemplo 4: Tarefa simples (sem orquestracao completa)

```
Voce: Corrija o typo no nome do campo "stauts" para "status" na entity Order.

Orchestrator:
  → Identifica como tarefa trivial
  → Age diretamente sem acionar todos os agentes
  → Corrige e sugere validacao
```

#### Exemplo 5: Acionar agente especifico diretamente

Se voce sabe que precisa apenas de uma perspectiva, instrua o Claude Code em linguagem natural para usar um agente especifico:

```
Voce: Usando o security-reviewer, revise a configuracao de autenticacao
      do endpoint /api/v1/payments.

  → Somente o security-reviewer analisa
  → Resposta focada em seguranca
```

> **Nota**: Sub-agentes no Claude Code nao tem sintaxe especial como `@nome`. Voce os aciona referenciando o nome do agente no texto da mensagem ou deixando o orquestrador decidir automaticamente com base no campo `description` de cada agente.

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
| `description` | **Campo critico.** O Claude Code usa esse campo para decidir automaticamente quando invocar o agente. Uma descricao clara com condicoes de uso ("use para X, Y, Z") melhora a selecao automatica. Descricoes vagas reduzem a chance de o agente ser acionado corretamente. |
| `tools` | Lista de ferramentas que o agente pode usar. Controla o que ele pode fazer. |
| `model` | Modelo Claude a ser usado (`opus`, `sonnet`, `haiku`). |

### 2. Corpo Markdown (instrucoes)

Apos o frontmatter, o conteudo Markdown define:

- **Papel** — o que o agente faz
- **Escopo** — o que ele deve revisar ou implementar
- **Regras mandatorias** — restricoes que ele deve seguir
- **Checklist** — itens que ele deve verificar
- **Formato de saida** — secoes obrigatorias na resposta

### Ferramentas disponiveis

| Ferramenta | O que faz | Quem usa |
|------------|-----------|----------|
| `Read` | Le arquivos | Todos |
| `Glob` | Busca arquivos por padrao | Todos |
| `Grep` | Busca conteudo em arquivos | Todos |
| `Edit` | Edita arquivos existentes | orchestrator, software-engineer, tech-writer |
| `Write` | Cria arquivos novos | orchestrator, software-engineer, tech-writer |
| `Bash` | Executa comandos no terminal | orchestrator, software-engineer, sre-platform, tech-writer |
| `Agent` | Invoca outros agentes | orchestrator (apenas ele) |
| `WebSearch` | Busca informacoes na web | dependency-versions-reviewer, data-engineering-aws-architect |
| `WebFetch` | Acessa URLs especificas | dependency-versions-reviewer, data-engineering-aws-architect |

**Decisao de design**: agentes de revisao so podem ler. Apenas o `software-engineer`, o `staff-engineer-orchestrator` e o `tech-writer` podem modificar arquivos. Isso evita que revisores facam mudancas sem consolidacao.

O `dependency-versions-reviewer` e o `data-engineering-aws-architect` usam `WebSearch`/`WebFetch` para consultar fontes externas atualizadas — nunca assumem versao ou preco por memoria do modelo.

### Escolha de modelo

| Modelo | Quando usar |
|--------|-------------|
| `opus` | Raciocinio complexo, consolidacao, decisoes arquiteturais. Usado no orquestrador e no data-engineering-aws-architect. |
| `sonnet` | Analise focada, revisao, implementacao. Usado nos demais especialistas. |
| `haiku` | Tarefas rapidas e simples. Nao usado aqui, mas disponivel. |

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
- Item 3

## Regras mandatorias

- Regra 1
- Regra 2
- Regra 3

## Checklist de revisao

- [ ] Check 1?
- [ ] Check 2?
- [ ] Check 3?

## Formato de saida obrigatorio

### 1. Secao 1
Descricao do que deve conter.

### 2. Secao 2
Descricao do que deve conter.
```

### Passo 4: Registre no orquestrador (se necessario)

Se o novo agente deve ser consultado pelo `staff-engineer-orchestrator`, edite o arquivo `.claude/agents/staff-engineer-orchestrator.md` e adicione-o na ordem de consulta.

### Passo 5: Atualize o CLAUDE.md (se necessario)

Se o agente e parte do fluxo padrao, adicione-o na lista de agentes do `CLAUDE.md`.

### Exemplo completo: agente de acessibilidade

```yaml
---
name: accessibility-reviewer
description: "Revisa acessibilidade de interfaces, contraste, navegacao por teclado e conformidade WCAG."
tools:
  - Read
  - Glob
  - Grep
model: sonnet
---

# Accessibility Reviewer

Voce e o accessibility reviewer. Seu papel e garantir conformidade
com WCAG 2.1 AA e boas praticas de acessibilidade.

## Escopo de revisao

- Contraste de cores
- Navegacao por teclado
- Screen readers
- Semantica HTML
- ARIA labels

## Regras mandatorias

- WCAG 2.1 AA como baseline
- Nao aceite "decorativo" como justificativa para falta de alt text
- Considere usuarios de screen reader em toda interacao

## Checklist de revisao

- [ ] Contraste minimo 4.5:1 para texto normal?
- [ ] Todos os elementos interativos acessiveis por teclado?
- [ ] Alt text em todas as imagens nao decorativas?
- [ ] Hierarquia de headings correta?
- [ ] ARIA labels quando semantica HTML nao e suficiente?

## Formato de saida obrigatorio

### 1. Diagnostico de acessibilidade
Avaliacao geral.

### 2. Violacoes criticas
Problemas que impedem uso por usuarios com deficiencia.

### 3. Melhorias recomendadas
Acoes com prioridade.
```

> **Lembre-se**: apos criar o arquivo, siga os Passos 4 e 5 acima para registrar o agente no `staff-engineer-orchestrator.md` e no `CLAUDE.md`. Sem isso, o agente existe mas nunca sera chamado pelo orquestrador.

---

## Anatomia da resposta do orquestrador

Toda resposta do `staff-engineer-orchestrator` segue **exatamente** esta estrutura:

```
1.  Diagnostico inicial                    → O que foi pedido e o contexto
2.  Stack e modulos impactados             → Tecnologias e areas afetadas
3.  Achados do Dependency Versions         → Versoes GA validadas via WebSearch
4.  Achados do Tech Lead                   → Pragmatismo e manutencao
5.  Achados do Architect                   → Arquitetura, boundaries, modelo de execucao
6.  Achados do API Contract                → Contratos, breaking changes, schema governance
7.  Achados do Security                    → Seguranca e riscos
8.  Achados do Compliance                  → LGPD, GDPR, serverless compliance
9.  Achados do AD/DBA                      → Dados e persistencia
10. Achados do Data Engineering            → Pipelines, Glue, EMR, Kinesis — omitir se nao aplicavel
11. Achados do Java Specialist             → Idiomatismo Java 25 — omitir se nao Java
12. Achados do Python Specialist           → Idiomatismo Python — omitir se nao Python
13. Achados do Go Specialist               → Idiomatismo Go — omitir se nao Go
14. Achados do Software Engineer           → Implementacao proposta
15. Achados do SRE/Platform                → Operabilidade e deploy
16. Achados do FinOps                      → Custo AWS, rightsizing
17. Achados do DevEx                       → Onboarding, ambiente local
18. Achados do QA/Quality                  → Testes e qualidade
19. Achados do Performance                 → Performance e confiabilidade
20. Achados do Tech Writer                 → Documentacao — omitir se nao aplicavel
21. Conflitos entre recomendacoes          → Divergencias e resolucao
22. Plano final priorizado                 → Acoes ordenadas por prioridade
23. Diff sugerido                          → Mudancas concretas
24. Riscos remanescentes                   → O que ainda pode dar errado
25. Estrategia de validacao                → Como confirmar que esta correto
26. Documentacao a atualizar               → Docs a criar/atualizar — omitir se nao aplicavel
```

Essa estrutura fixa garante:
- **Rastreabilidade**: voce sabe de onde veio cada recomendacao
- **Auditabilidade**: facil comparar analises entre demandas diferentes
- **Completude**: nenhuma perspectiva e ignorada silenciosamente

As secoes de especialistas de linguagem (11–13), data engineering (10), tech writer (20) e documentacao (26) sao omitidas quando nao aplicaveis, mantendo a resposta enxuta.

---

## Papel do CLAUDE.md

O `CLAUDE.md` e o documento de governanca do projeto. O Claude Code le esse arquivo automaticamente ao abrir o repositorio.

Ele define:

| Secao | O que faz |
|-------|-----------|
| Agente principal | Quem coordena |
| Stack oficial | Java, Python, Go, AWS Serverless |
| Regras de bordas | `web/` e `message/` como bordas da aplicacao |
| Organizacao arquitetural | Onde cada coisa fica |
| Checklist transversal | O que toda proposta deve validar |
| Ordem de consulta | Sequencia dos 19 agentes |
| Regras de execucao | Comportamentos obrigatorios |
| Regras por framework | Idiomatismo de cada tecnologia |

**Todos os agentes respeitam o CLAUDE.md.** Se voce mudar uma regra la, todos os agentes passam a segui-la.

---

## Customizacao

### Mudar o agente padrao

Edite `.claude/settings.json`:

```json
{
  "defaultAgent": "outro-agente"
}
```

### Mudar o modelo de um agente

Edite o frontmatter do agente:

```yaml
model: opus    # mais capaz, mais lento, mais caro
model: sonnet  # equilibrado (padrao dos especialistas)
model: haiku   # mais rapido, mais barato, menos capaz
```

### Adicionar ferramentas a um agente

Edite o frontmatter:

```yaml
tools:
  - Read
  - Glob
  - Grep
  - Edit      # agora o agente pode editar arquivos
  - Bash      # agora o agente pode executar comandos
  - WebSearch # agora o agente pode buscar na web
```

### Remover um agente do fluxo

1. Remova da lista de consulta no `staff-engineer-orchestrator.md`
2. Remova da lista no `CLAUDE.md`
3. Opcionalmente, delete o arquivo `.claude/agents/nome.md`

---

## Perguntas frequentes

### Preciso acionar todos os agentes sempre?

Nao. O orquestrador decide quais agentes sao relevantes para cada demanda. Para uma mudanca so de banco de dados, ele pode acionar apenas `ad-dba-reviewer`, `software-engineer` e `qa-quality-engineer`.

### Posso usar sem o orquestrador?

Sim. Voce pode acionar qualquer agente diretamente. O orquestrador e o fluxo recomendado para demandas complexas, mas nao e obrigatorio.

### Funciona com Java, Python e Go nativamente?

Sim. A estrutura tem suporte nativo a stack poliglota. Ha especialistas dedicados para cada linguagem (`java-specialist`, `python-specialist`, `go-specialist`) e todos os agentes de revisao foram escritos considerando os tres ecossistemas. AWS Serverless (Lambda, API Gateway, EventBridge, SQS, DynamoDB, S3) tambem e suportado nativamente.

### O que e o dependency-versions-reviewer?

Um agente especial que usa `WebSearch` para verificar a versao GA mais recente de qualquer dependencia — Spring Boot, Quarkus, boto3, runtimes AWS, etc. Ele e acionado obrigatoriamente antes de qualquer implementacao que envolva dependencias, porque o knowledge cutoff do modelo pode estar desatualizado.

### O que e o data-engineering-aws-architect?

Um especialista em data platform e engenharia de dados na AWS. Ele decide com precisao entre Glue, EMR Serverless, EMR on EC2, Lambda e Step Functions para pipelines de dados, justificando trade-offs tecnicos, operacionais e financeiros. Usa `opus` como modelo e `WebSearch` para verificar precos e servicos AWS atualizados.

### Quanto custa em tokens?

Depende da demanda. Uma analise completa com todos os agentes consome significativamente mais tokens que um unico agente. Para tarefas simples, o custo extra nao se justifica — por isso o orquestrador tem a regra de agir diretamente em tarefas triviais.

### Posso usar em outro repositorio?

Sim. Copie a pasta `.claude/` e o `CLAUDE.md` para outro repo e adapte o conteudo. A estrutura e agnositca — usa `<project-root>/` e `<base-package>/` como placeholders.

---

## Referencias

- [Claude Code — Documentacao oficial](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code — Custom Agents](https://docs.anthropic.com/en/docs/claude-code/agents)
- [Claude Code — CLAUDE.md](https://docs.anthropic.com/en/docs/claude-code/memory)
