# Multi-Agent Orchestration para Gemini CLI

## O que é isso?

Uma estrutura de **orquestração multiagente** nativa para o [Gemini CLI](https://github.com/google/gemini-cli) que simula um **time de engenharia completo** dentro do seu terminal.

Em vez de um único agente fazendo tudo, você tem **24 agentes especializados** — cada um com papel, escopo, checklist e formato de saída definidos — coordenados por um **orquestrador principal** (o `staff-engineer-orchestrator`) que funciona como maestro.

Além dos agentes, o projeto inclui **33 slash commands customizados**, **45 skills globais reutilizáveis**, **permissões granulares**, **hooks de segurança** e uma configuração completa para workflow profissional.

### Analogia simples

Imagine que você tem uma demanda técnica complexa. Em vez de pedir para um único engenheiro resolver tudo sozinho, você:

1. Leva a demanda para o **staff engineer** (orquestrador)
2. Ele distribui a análise para os especialistas do time
3. Cada especialista analisa sob sua perspectiva
4. O staff engineer consolida tudo, resolve conflitos e entrega o plano final

Isso é exatamente o que essa estrutura faz — automaticamente, dentro do Gemini CLI.

---

## Por que usar?

### O problema

Quando você usa um único agente de IA para tarefas complexas:

- Ele tenta resolver tudo de uma vez, sem análise adequada
- Perde perspectivas importantes (segurança, performance, operabilidade)
- Não diferencia risco crítico de melhoria futura
- Não considera trade-offs sob múltiplas perspectivas
- Tende a overengineering ou a soluções incompletas

### A solução

Com multiagentes, cada especialista foca no que sabe. O orquestrador garante que nenhuma perspectiva é ignorada e que a resposta final é consolidada e priorizada.

### Ganhos concretos

| Ganho | Descrição |
|-------|-----------|
| **Cobertura ampla** | 24 perspectivas especializadas em vez de uma genérica |
| **Stack poliglota** | Suporte nativo a Java, Python, Go, Frontend, Mobile e AWS Serverless |
| **Slash commands** | Atalhos para ações frequentes — `/review`, `/implement`, `/debug`, `/refactor`, etc. |
| **Segurança integrada** | Hooks que bloqueiam edição de arquivos sensíveis e alertam sobre segredos |
| **Qualidade de análise** | Cada agente tem checklist e regras mandatórias do seu domínio |
| **Rastreabilidade** | Saída estruturada com seções fixas — fácil de auditar e comparar |
| **Conflitos explícitos** | Quando dois agentes discordam, o orquestrador explicita e resolve |
| **Priorização** | Plano final ordenado por prioridade com justificativa |
| **Riscos visíveis** | Riscos remanescentes listados explicitamente |
| **Reproducibilidade** | Mesma estrutura de resposta toda vez, independente da demanda |
| **Escalabilidade do time** | Fácil adicionar novos agentes sem quebrar o fluxo |

**Regra prática**: use o orquestrador para demandas não triviais. Para tarefas simples, use um slash command direto ou acione o agente relevante.

---

## Estrutura do repositório

```
.
├── GEMINI.md                                          # Governança do projeto e diretrizes de orquestração
├── README.md                                          # Este arquivo
└── .gemini/
    ├── settings.json                                  # Permissões, hooks e configuração do CLI
    ├── commands/                                      # Slash commands customizados (workflows e reviews)
    │   ├── reviews/                                   # Comandos de revisão (arch-review, security-check, etc)
    │   │   └── arch-review.toml                       # Exemplo de revisão arquitetural
    │   ├── roles/                                     # Comandos para invocar os especialistas diretamente
    │   └── workflows/                                 # Comandos operacionais (debug, refactor, implement, etc)
    │       └── implement.toml                         # Exemplo de comando de workflow
    ├── agents/                                        # 24 agentes especializados em Markdown
    │   ├── staff-engineer-orchestrator.md             # Maestro principal
    │   ├── dependency-versions-reviewer.md            # Versões GA de dependências
    │   ├── tech-lead-reviewer.md                      # Pragmatismo e manutenibilidade
    │   ├── architect-reviewer.md                      # Arquitetura e boundaries
    │   ├── api-contract-reviewer.md                   # Contratos de borda e schema governance
    │   ├── security-reviewer.md                       # Segurança e hardening
    │   ├── compliance-reviewer.md                     # LGPD, GDPR, compliance
    │   ├── ad-dba-reviewer.md                         # Dados e persistência
    │   ├── data-engineering-aws-architect.md          # Pipelines de dados
    │   ├── java-specialist.md                         # Java 25, Spring Boot, Quarkus, Micronaut
    │   ├── jakarta-ee-specialist.md                   # Jakarta EE 11, MicroProfile
    │   ├── python-specialist.md                       # Python, FastAPI, Pytest
    │   ├── go-specialist.md                           # Go, go.mod, testing
    │   ├── frontend-specialist.md                     # React, Angular
    │   ├── mobile-native-specialist.md                # Android, iOS
    │   ├── software-engineer.md                       # Implementação mínima correta
    │   ├── sre-platform-engineer.md                   # Operabilidade, IaC
    │   ├── cicd-pipeline-engineer.md                  # Deploy, rollback
    │   ├── incident-response-reviewer.md              # SLOs, runbooks
    │   ├── finops-reviewer.md                         # Custo AWS
    │   ├── devex-reviewer.md                          # Onboarding, dev local
    │   ├── qa-quality-engineer.md                     # Testes e qualidade
    │   ├── performance-reliability-reviewer.md        # Performance
    │   └── tech-writer.md                             # Documentação técnica
    └── skills/                                        # 45 skills globais reutilizáveis
        ├── java-spring-patterns.md
        ├── python-fastapi-patterns.md
        ├── aws-architecture-patterns.md
        ├── code-review.md
        └── ...
```

---

## Slash Commands — Referência rápida

### Orquestração

| Comando | Agente(s) | Propósito |
|---------|-----------|-----------|
| `/review` | staff-engineer-orchestrator | Revisão inteligente com triage automático |
| `/full-review` | staff-engineer-orchestrator | Revisão completa — todos os agentes relevantes |
| `/implement` | staff-engineer-orchestrator | Análise + implementação de demanda |
| `/pre-pr` | staff-engineer-orchestrator | Checklist GO/NO-GO antes de abrir PR |

### Revisões especializadas

| Comando | Agente(s) | Propósito |
|---------|-----------|-----------|
| `/arch-review` | architect-reviewer | Arquitetura, boundaries, trade-offs |
| `/security-check` | security-reviewer | Segurança, OWASP, hardening |
| `/compliance` | compliance-reviewer | LGPD/GDPR, residência de dados |
| `/contract-review` | api-contract-reviewer | Contratos, breaking changes, schema |
| `/check-deps` | dependency-versions-reviewer | Versões GA via WebSearch |
| `/data-review` | ad-dba-reviewer | Dados, persistência, modelagem |
| `/qa-review` | qa-quality-engineer | Testes, edge cases, regressões |
| `/perf-review` | performance-reliability-reviewer | Throughput, latência, escalabilidade |
| `/sre-review` | sre-platform-engineer | Operabilidade, deploy, observabilidade |
| `/cicd-review` | cicd-pipeline-engineer | Pipelines CI/CD, deploy strategy |

### Workflows de desenvolvimento

| Comando | Tipo | Propósito |
|---------|------|-----------|
| `/debug` | Workflow | Investigação sistemática de causa raiz com reprodução |
| `/refactor` | Workflow | Refatoração segura com mapeamento de dependentes |
| `/scaffold` | Workflow | Criar novo módulo/componente seguindo padrões |
| `/test-gen` | Workflow | Gerar ou melhorar testes com cobertura de comportamentos |

Todos os comandos aceitam argumentos diretos. Exemplo: `/debug o endpoint /orders retorna 500 quando o payload tem campo opcional nulo`

---

## Permissões e Segurança

### Permissões (`.gemini/settings.json`)

O projeto configura permissões e limites para evitar operações danosas e garantir fluidez nas ações rotineiras:

**Ferramentas Essenciais Permitidas:**
- `run_shell_command`, `read_file`, `write_file`, `replace`
- `glob`, `grep_search`, `list_directory`
- `google_web_search`, `web_fetch`

### Hooks de segurança

O `settings.json` inclui hooks automáticos do tipo `BeforeTool` e `AfterTool` para monitoramento constante:

| Hook | Trigger | Ação |
|------|---------|------|
| BeforeTool | `replace` ou `write_file` | **Bloqueia** edição de arquivos sensíveis (`.env`, `.pem`, `.key`, `.secret`, `.credentials`, `.token`) |
| AfterTool | `run_shell_command` | **Alerta** no console se o output contiver possíveis segredos vazados (AWS_SECRET_ACCESS_KEY, PRIVATE.KEY, etc.) |

---

## Como os agentes são definidos

Cada agente é um arquivo Markdown em `.gemini/agents/`. O conteúdo é apenas texto focado nas instruções, otimizado para o Gemini CLI.

O corpo Markdown define:
- **Papel** — o que o agente faz
- **Escopo** — o que ele deve revisar ou implementar
- **Stack e contexto** — tecnologias que ele conhece
- **Regras mandatórias** — restrições que ele deve seguir
- **Checklist** — itens que ele deve verificar
- **Modo rápido** — formato compacto para respostas breves
- **Formato de saída** — seções obrigatórias na resposta

---

## Como adicionar novas configurações

Todos os pontos de extensão do Gemini CLI neste projeto.

### 1. Novo agente

**Arquivo**: `.gemini/agents/<nome-do-agente>.md`

```markdown
# Meu Novo Agente

Você é o [papel] de um sistema crítico, com stack poliglota (Java, Python, Go) e suporte a AWS Serverless.

## Escopo de revisão
- Item 1
- Item 2

## Regras mandatórias
- Regra 1

## Checklist de revisão
- [ ] Check 1?

## Modo rápido
- **Veredicto**: uma linha
- 3 bullets + ação prioritária

## Formato de saída obrigatório
### 1. Seção 1
### 2. Seção 2
```

**Registrar o agente**:
1. Adicionar na ordem de consulta do `.gemini/agents/staff-engineer-orchestrator.md`.
2. Criar um comando correspondente em `.gemini/commands/roles/<nome>.toml` apontando para o agente.
3. Atualizar o `GEMINI.md` com o novo papel.

---

### 2. Novo slash command

Os comandos ficam em `.gemini/commands/<categoria>/<nome>.toml`. Categorias em uso:

| Pasta | Proposito | Exemplos |
|-------|-----------|----------|
| `orchestrate/` | Entradas de alto nivel | `review-architecture`, `upgrade-plan` |
| `reviews/` | Revisoes especializadas | `arch-review`, `security-check`, `qa-review` |
| `roles/` | Invocar um especialista diretamente | `ad-dba-reviewer`, `security-reviewer` |
| `workflows/` | Operacoes e investigacoes | `debug`, `refactor`, `implement`, `test-gen` |

**Comando do tipo `roles/` (delegação a um agente)**:

```toml
description = "Consulta o Meu Novo Agente sobre [foco]"
prompt = """
@{agents/meu-novo-agente.md}

Você é o Meu Novo Agente conforme definido acima. Foco em [objetivo].
"""
```

**Comando do tipo `workflows/` (fluxo operacional)**:

```toml
description = "Descrição curta do que o comando faz"
prompt = """
Instruções passo a passo do workflow.

## Agentes disponíveis (quando necessário)
- Para segurança: acione `@{agents/security-reviewer.md}`
- Para implementação: use `@{agents/software-engineer.md}`

## Entrada do usuário
$ARGUMENTS
"""
```

A diretiva `@{agents/<nome>.md}` importa o conteúdo do agente. `$ARGUMENTS` captura o texto que o usuário digita após o comando.

---

### 3. Nova skill

**Arquivo**: `.gemini/skills/<nome>/SKILL.md` (ou `.gemini/skills/<nome>.md` para skills simples)

```markdown
---
name: minha-skill
description: Conhecimento procedural reutilizável sobre X. Dispara quando o contexto envolve Y.
---

# Skill: minha-skill

## Quando aplicar
- Contexto A
- Contexto B

## Conteúdo
Passos, exemplos e templates reutilizáveis.
```

Skills são carregadas automaticamente quando o contexto corresponde ao `description` — não exigem registro em `settings.json`.

---

### 4. Nova permissão de ferramenta

Edite `.gemini/settings.json`:

```jsonc
{
  "tools": {
    "allowed": [
      "run_shell_command",
      "google_web_search",
      "web_fetch",
      "read_file",
      "write_file",
      "replace",
      "glob",
      "grep_search",
      "list_directory",
      "minha_ferramenta_nova"
    ]
  }
}
```

Apenas ferramentas listadas em `tools.allowed` podem ser acionadas pelos agentes.

---

### 5. Novo hook

Edite `.gemini/settings.json`:

```jsonc
{
  "hooks": {
    "BeforeTool": [
      {
        "matcher": "write_file|replace",
        "hooks": [
          {
            "type": "command",
            "command": "powershell -NoProfile -Command \"... política ...\""
          }
        ]
      }
    ],
    "AfterTool": [
      {
        "matcher": "run_shell_command",
        "hooks": [
          {
            "type": "command",
            "command": "powershell -NoProfile -Command \"... auditoria ...\""
          }
        ]
      }
    ]
  }
}
```

`BeforeTool` pode bloquear a ação (exit != 0). `AfterTool` roda após a execução — útil para alertas e auditoria.

---

### 6. Atualizar o GEMINI.md

Toda mudança em governança (novo papel, nova regra transversal, mudança de fluxo) deve refletir no `GEMINI.md`. Ele é lido automaticamente pelo Gemini CLI no início da sessão.

---

### Checklist antes de mergear

- [ ] Arquivo do agente em `.gemini/agents/` + comando em `.gemini/commands/roles/`?
- [ ] `GEMINI.md` atualizado com o novo papel?
- [ ] Ordem de consulta do `staff-engineer-orchestrator.md` atualizada?
- [ ] Comando TOML tem `description` e `prompt` claros?
- [ ] Skill tem `description` específico para ativação correta?
- [ ] `settings.json` ajustado se a nova config precisa de ferramenta ou hook novo?
- [ ] README atualizado com contagens e propósito do novo item?
- [ ] Paridade com as outras plataformas (`claude-code/`, `codex/`, `copilot/`)?

---

## Papel do GEMINI.md

O `GEMINI.md` é o documento de governança do projeto. O Gemini CLI lê esse arquivo automaticamente para injetar contexto global na sessão.

Todos os agentes respeitam as diretrizes consolidadas no `GEMINI.md`.

## Referências

- [Gemini CLI — GitHub](https://github.com/google/gemini-cli)
