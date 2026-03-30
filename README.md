# Multi-Agent Orchestration para Claude Code

## O que e isso?

Uma estrutura de **orquestracao multiagente** para o [Claude Code](https://docs.anthropic.com/en/docs/claude-code) que simula um **time de engenharia completo** dentro do seu terminal.

Em vez de um unico agente fazendo tudo, voce tem **10 agentes especializados** — cada um com papel, escopo, checklist e formato de saida definidos — coordenados por um **orquestrador principal** (o `staff-engineer-orchestrator`) que funciona como maestro.

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
| **Cobertura ampla** | 9 perspectivas especializadas em vez de uma generica |
| **Qualidade de analise** | Cada agente tem checklist e regras mandatorias do seu dominio |
| **Rastreabilidade** | Saida estruturada com secoes fixas — facil de auditar e comparar |
| **Conflitos explicitos** | Quando dois agentes discordam, o orquestrador explicita e resolve |
| **Priorizacao** | Plano final ordenado por prioridade com justificativa |
| **Riscos visiveis** | Riscos remanescentes listados explicitamente |
| **Reprodutibilidade** | Mesma estrutura de resposta toda vez, independente da demanda |
| **Escalabilidade do time** | Facil adicionar novos agentes sem quebrar o fluxo |

### Trade-offs

| Trade-off | Descricao |
|-----------|-----------|
| **Latencia** | Multiplos agentes = mais tempo de resposta. Para tarefas triviais, pode ser excessivo |
| **Custo de tokens** | Cada agente consome tokens. Demandas simples custam mais que o necessario |
| **Complexidade inicial** | Precisa entender a estrutura antes de usar com eficiencia |
| **Maturidade do Claude Code** | O recurso de agentes customizados ainda esta em evolucao |
| **Overhead para tarefas simples** | Para um bugfix pontual, acionar 9 agentes e desproporcional |

**Regra pratica**: use o orquestrador para demandas nao triviais. Para tarefas simples, acione diretamente o agente relevante.

---

## Estrutura do repositorio

```
.
├── CLAUDE.md                                    # Governanca do projeto
├── README.md                                    # Este arquivo
└── .claude/
    ├── settings.json                            # Configuracao do Claude Code
    └── agents/                                  # Agentes especializados
        ├── staff-engineer-orchestrator.md             # Maestro principal
        ├── tech-lead-reviewer.md                 # Pragmatismo e manutenibilidade
        ├── architect-reviewer.md                 # Arquitetura e boundaries
        ├── api-contract-reviewer.md              # Contratos de borda e schema governance
        ├── security-reviewer.md                  # Seguranca e hardening
        ├── ad-dba-reviewer.md                    # Dados e persistencia
        ├── software-engineer.md                  # Implementacao
        ├── sre-platform-engineer.md              # Operabilidade e plataforma
        ├── qa-quality-engineer.md                # Testes e qualidade
        └── performance-reliability-reviewer.md   # Performance e confiabilidade
```

### O que cada arquivo faz

| Arquivo | Funcao |
|---------|--------|
| `CLAUDE.md` | Documento de governanca lido automaticamente pelo Claude Code. Define stack, regras arquiteturais, checklists transversais e ordem de consulta dos agentes. Todo agente respeita o que esta aqui. |
| `.claude/settings.json` | Configura o `staff-engineer-orchestrator` como agente padrao do projeto. Quando voce abre o Claude Code neste repo, ele ja sabe qual agente usar. |
| `.claude/agents/*.md` | Cada arquivo define um agente com: papel, escopo, regras, checklist e formato de saida obrigatorio. |

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
  ┌─────┬──────┼──────┬──────┬──────┬──────┬──────┬──────┐
  ▼     ▼      ▼      ▼      ▼      ▼      ▼      ▼      ▼
tech- archi-  api-  securi- ad-   soft-   sre-   qa-   perfor-
lead  tect   cont-  ty     dba   ware   plat-  quali- mance
             ract               eng    form   ty
  │     │      │      │      │      │      │      │      │
  └─────┴──────┴──────┴──────┴──────┴──────┴──────┴──────┘
                │
                ▼
┌──────────────────────────────────┐
│  staff-engineer-orchestrator     │  ← Consolida, resolve conflitos, prioriza
└───────────────┬──────────────────┘
                │
                ▼
    Resposta final estruturada (16 secoes)
```

### Ordem de consulta

O orquestrador segue esta ordem preferencial:

| # | Agente | Foco |
|---|--------|------|
| 1 | `tech-lead-reviewer` | Pragmatismo, simplicidade, custo de manutencao |
| 2 | `architect-reviewer` | Boundaries, acoplamento, resiliencia, contratos |
| 3 | `api-contract-reviewer` | Contratos de borda, breaking changes, schema governance |
| 4 | `security-reviewer` | Seguranca, hardening, superficies de abuso |
| 5 | `ad-dba-reviewer` | Dados, modelagem, queries, indices, CAP theorem |
| 6 | `software-engineer` | Implementacao minima correta |
| 7 | `sre-platform-engineer` | Operabilidade, deploy, observabilidade, IaC |
| 8 | `qa-quality-engineer` | Testes, edge cases, regressoes |
| 9 | `performance-reliability-reviewer` | Throughput, latencia, escalabilidade |

---

## Como usar

### Pre-requisitos

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) instalado
- Repositorio clonado localmente

### Uso basico

```bash
# 1. Clone o repositorio
git clone <repo-url>
cd multi-agents

# 2. Abra o Claude Code
claude

# 3. O staff-engineer-orchestrator ja e o agente padrao.
#    Basta fazer sua pergunta ou pedir uma implementacao.
```

### Exemplos de uso

#### Exemplo 1: Analise de uma nova feature

```
Voce: Preciso adicionar um endpoint REST para consulta de pedidos
      com paginacao, filtro por status e ordenacao por data.

Orchestrator:
  → Aciona tech-lead-reviewer (simplicidade, padroes)
  → Aciona architect-reviewer (boundaries, contratos REST)
  → Aciona api-contract-reviewer (OpenAPI, breaking changes)
  → Aciona security-reviewer (validacao, autorizacao)
  → Aciona ad-dba-reviewer (query, indice, paginacao)
  → Aciona software-engineer (implementacao)
  → Aciona sre-platform-engineer (metricas, observabilidade)
  → Aciona qa-quality-engineer (testes)
  → Aciona performance-reliability-reviewer (latencia, N+1)

  → Consolida tudo em resposta com 16 secoes
```

#### Exemplo 2: Revisao de codigo existente

```
Voce: Revise o consumer Kafka que processa eventos de pagamento.
      Quero saber se esta resiliente e seguro para producao.

Orchestrator:
  → Aciona tech-lead-reviewer (complexidade, manutencao)
  → Aciona architect-reviewer (bordas assincronas, idempotencia)
  → Aciona security-reviewer (dados sensiveis em logs, payload)
  → Aciona sre-platform-engineer (DLQ, metricas, lag)
  → Aciona qa-quality-engineer (testes de falha, reprocessamento)
  → Aciona performance-reliability-reviewer (throughput, backpressure)

  → Consolida com riscos priorizados e plano de acao
```

#### Exemplo 3: Tarefa simples (sem orquestracao completa)

```
Voce: Corrija o typo no nome do campo "stauts" para "status" na entity Order.

Orchestrator:
  → Identifica como tarefa trivial
  → Age diretamente sem acionar todos os agentes
  → Corrige e sugere validacao
```

#### Exemplo 4: Acionar agente especifico diretamente

Se voce sabe que precisa apenas de uma perspectiva, pode acionar o agente diretamente no Claude Code:

```
Voce: @security-reviewer Revise a configuracao de autenticacao
      do endpoint /api/v1/payments

  → Somente o security-reviewer analisa
  → Resposta focada em seguranca
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
| `description` | Descricao curta exibida no Claude Code. |
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
| `Edit` | Edita arquivos existentes | orchestrator, software-engineer |
| `Write` | Cria arquivos novos | orchestrator, software-engineer |
| `Bash` | Executa comandos no terminal | orchestrator, software-engineer, sre-platform |
| `Agent` | Invoca outros agentes | orchestrator (apenas ele) |

**Decisao de design**: agentes de revisao so podem ler. Apenas o `software-engineer` e o `staff-engineer-orchestrator` podem modificar arquivos. Isso evita que revisores facam mudancas sem consolidacao.

> O `api-contract-reviewer` tambem e somente leitura — ele revisa contratos (OpenAPI, Protobuf, GraphQL Schema, Avro, AsyncAPI, JSON Schema) mas nao os modifica diretamente.

### Escolha de modelo

| Modelo | Quando usar |
|--------|-------------|
| `opus` | Raciocinio complexo, consolidacao, decisoes arquiteturais. Usado no orquestrador. |
| `sonnet` | Analise focada, revisao, implementacao. Usado nos especialistas. |
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

Voce e o [papel] de um sistema critico Java. Seu papel e [descricao clara].

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

---

## Anatomia da resposta do orquestrador

Toda resposta do `staff-engineer-orchestrator` segue **exatamente** esta estrutura:

```
1.  Diagnostico inicial           → O que foi pedido e o contexto
2.  Stack e modulos impactados    → Tecnologias e areas afetadas
3.  Achados do Tech Lead          → Pragmatismo e manutencao
4.  Achados do Architect          → Arquitetura e boundaries
5.  Achados do API Contract       → Contratos, breaking changes, schema governance
6.  Achados do Security           → Seguranca e riscos
7.  Achados do AD/DBA             → Dados e persistencia
8.  Achados do Software Engineer  → Implementacao proposta
9.  Achados do SRE/Platform       → Operabilidade e deploy
10. Achados do QA/Quality         → Testes e qualidade
11. Achados do Performance        → Performance e confiabilidade
12. Conflitos entre recomendacoes → Divergencias e resolucao
13. Plano final priorizado        → Acoes ordenadas por prioridade
14. Diff sugerido                 → Mudancas concretas
15. Riscos remanescentes          → O que ainda pode dar errado
16. Estrategia de validacao       → Como confirmar que esta correto
```

Essa estrutura fixa garante:
- **Rastreabilidade**: voce sabe de onde veio cada recomendacao
- **Auditabilidade**: facil comparar analises entre demandas diferentes
- **Completude**: nenhuma perspectiva e ignorada silenciosamente

---

## Papel do CLAUDE.md

O `CLAUDE.md` e o documento de governanca do projeto. O Claude Code le esse arquivo automaticamente ao abrir o repositorio.

Ele define:

| Secao | O que faz |
|-------|-----------|
| Agente principal | Quem coordena |
| Stack oficial | Tecnologias do projeto |
| Regras de bordas | `web/` e `message/` como bordas da aplicacao |
| Organizacao arquitetural | Onde cada coisa fica |
| Checklist transversal | O que toda proposta deve validar |
| Ordem de consulta | Sequencia dos agentes |
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
  - Edit     # agora o agente pode editar arquivos
  - Bash     # agora o agente pode executar comandos
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

### Funciona com qualquer linguagem?

A estrutura de agentes (`.claude/agents/*.md`) funciona com qualquer projeto no Claude Code. O **conteudo** destes agentes foi escrito para Java (Spring Boot, Quarkus, Micronaut), mas voce pode adaptar para qualquer stack editando os arquivos.

### Quanto custa em tokens?

Depende da demanda. Uma analise completa com 9 agentes consome significativamente mais tokens que um unico agente. Para tarefas simples, o custo extra nao se justifica — por isso o orquestrador tem a regra de agir diretamente em tarefas triviais.

### Posso usar em outro repositorio?

Sim. Copie a pasta `.claude/` e o `CLAUDE.md` para outro repo e adapte o conteudo. A estrutura e agnositca — usa `<project-root>/` e `<base-package>/` como placeholders.

---

## Referencias

- [Claude Code — Documentacao oficial](https://docs.anthropic.com/en/docs/claude-code)
- [Claude Code — Custom Agents](https://docs.anthropic.com/en/docs/claude-code/agents)
- [Claude Code — CLAUDE.md](https://docs.anthropic.com/en/docs/claude-code/memory)
