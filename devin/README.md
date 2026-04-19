# Multi-Agent Orchestration para Devin CLI

## O que é isso?

Uma estrutura de **orquestração multiagente** para o [Devin CLI](https://cli.devin.ai/docs) que simula um **time de engenharia completo** dentro do seu terminal.

Em vez de um único agente fazendo tudo, você tem **24 subagentes especializados** — cada um com papel, escopo, checklist e formato de saída definidos — coordenados por um **orquestrador principal** (o `staff-engineer-orchestrator`).

Além dos subagentes, o projeto inclui **79 skills** (slash commands + conhecimento procedural), **permissões granulares**, **hooks de segurança** e uma configuração completa para workflow profissional.

Este módulo é uma adaptação do setup `claude-code/` para o modelo operacional do Devin CLI: `AGENT.md` no lugar de `.claude/agents/*.md`, `SKILL.md` no lugar de `.claude/commands/` + `.claude/skills/`, e `.devin/config.json` no lugar de `.claude/settings.json`.

---

## Estrutura do repositório

```
devin/
├── AGENTS.md                                         # Governança (lido automaticamente pelo Devin CLI)
├── README.md                                         # Este arquivo
└── .devin/
    ├── config.json                                   # Permissões, hooks, read_config_from
    ├── config.local.json                             # (gitignored) overrides pessoais
    ├── agents/                                       # 24 subagentes especializados
    │   ├── staff-engineer-orchestrator/AGENT.md      # Maestro principal (opus)
    │   ├── dependency-versions-reviewer/AGENT.md
    │   ├── tech-lead-reviewer/AGENT.md
    │   ├── architect-reviewer/AGENT.md
    │   ├── api-contract-reviewer/AGENT.md
    │   ├── security-reviewer/AGENT.md
    │   ├── compliance-reviewer/AGENT.md
    │   ├── ad-dba-reviewer/AGENT.md
    │   ├── data-engineering-aws-architect/AGENT.md   # (opus)
    │   ├── java-specialist/AGENT.md
    │   ├── jakarta-ee-specialist/AGENT.md
    │   ├── python-specialist/AGENT.md
    │   ├── go-specialist/AGENT.md
    │   ├── frontend-specialist/AGENT.md
    │   ├── mobile-native-specialist/AGENT.md
    │   ├── software-engineer/AGENT.md
    │   ├── sre-platform-engineer/AGENT.md
    │   ├── cicd-pipeline-engineer/AGENT.md
    │   ├── incident-response-reviewer/AGENT.md
    │   ├── finops-reviewer/AGENT.md
    │   ├── devex-reviewer/AGENT.md
    │   ├── qa-quality-engineer/AGENT.md
    │   ├── performance-reliability-reviewer/AGENT.md
    │   └── tech-writer/AGENT.md
    └── skills/                                       # 79 skills (invocadas via /nome)
        ├── review/SKILL.md                           # /review — revisão inteligente da branch
        ├── full-review/SKILL.md                      # /full-review — revisão completa
        ├── implement/SKILL.md                        # /implement — análise + implementação
        ├── pre-pr/SKILL.md                           # /pre-pr — checklist GO/NO-GO
        ├── arch-review/SKILL.md
        ├── security-check/SKILL.md
        ├── compliance/SKILL.md
        ├── check-deps/SKILL.md
        ├── debug/SKILL.md
        ├── refactor/SKILL.md
        ├── test-gen/SKILL.md
        └── ... (mais 68 skills — workflows, revisões, padrões Java/Python/Go/AWS/mobile/frontend, QA, arquitetura)
```

---

## Permissões e Segurança

### Permissões (`.devin/config.json`)

O setup usa três camadas: `allow` (automático), `ask` (pede confirmação) e `deny` (bloqueado).

**Allow (automático):**
- Leitura, busca, listagem (`Read(**)`, `Grep(**)`, `Glob(**)`)
- Ferramentas de build: `git`, `make`, `docker`, `mvn`, `gradle`, `go`, `python`, `npm`, `terraform`, `aws`, `gh`
- Comandos utilitários: `ls`, `cat`, `mkdir`, `cp`, `mv`, `find`, `curl`, `jq`, `which`
- `Fetch` para 16 domínios confiáveis (Maven Central, PyPI, npm, Go pkg, Terraform Registry, Docker Hub, docs AWS, Spring, Quarkus, Micronaut, Jakarta EE, MicroProfile)

**Ask (confirmação manual):**
- `Write(**)` e `Edit(**)` — toda escrita passa por aprovação

**Deny (bloqueado):**
- `rm -rf /`, `rm -rf .`, `git push --force`, `git reset --hard`
- Escrita/edição em `.env`, `.pem`, `.key`, `.secret`, `.credentials`, `.token`

### Hooks de segurança

| Hook | Evento | Ação |
|------|--------|------|
| PreToolUse | Antes de `write`/`edit` | **Bloqueia** se o path for de arquivo sensível |
| PostToolUse | Depois de `exec` | **Alerta** se o output contém possíveis segredos |

Hooks recebem JSON via stdin (`tool_name`, `tool_input`, `tool_response`) e retornam decisão via stdout.

---

## Como adicionar novas configurações

Todos os pontos de extensão do Devin CLI neste projeto.

### 1. Novo subagente

**Arquivo**: `.devin/agents/<nome>/AGENT.md`

```markdown
---
name: meu-novo-agente
description: "Descricao curta. Use para X, Y, Z."
model: sonnet
allowed-tools:
  - read
  - grep
  - glob
permissions:
  allow:
    - Read(**)
    - Exec(git)
  deny:
    - write
    - edit
---

# Meu Novo Agente

Voce e o [papel] de um sistema critico, com stack poliglota (Java, Python, Go) e suporte a AWS Serverless. Seu papel e [descricao clara].

## Escopo de revisao
- Item 1
- Item 2

## Regras mandatorias
- Regra 1

## Checklist de revisao
- [ ] Check 1?

## Modo rapido
- **Veredicto**: uma linha
- Maximo 3 bullets
- Acao prioritaria em 1 frase

## Formato de saida obrigatorio
### 1. Secao 1
### 2. Secao 2
```

**Campos do frontmatter**:

| Campo | Obrigatório | Descrição |
|-------|-------------|-----------|
| `name` | sim | Identificador único (bate com o nome da pasta) |
| `description` | sim | Usado na seleção automática de subagentes |
| `model` | não | `sonnet`, `opus` ou nome completo (ex: `claude-sonnet-4-6`) |
| `allowed-tools` | não | Subset de: `read`, `write`, `edit`, `grep`, `glob`, `exec`, `fetch` |
| `permissions` | não | Overrides finos no padrão `allow`/`ask`/`deny` |

**Registrar o subagente**:
1. Adicionar na ordem de consulta no `AGENTS.md` (seção "Ordem Padrão de Consulta")
2. Adicionar no body do `staff-engineer-orchestrator/AGENT.md` (seção de delegação)
3. (Opcional) Criar uma skill dedicada em `.devin/skills/` para invocação direta

---

### 2. Nova skill (slash command)

**Arquivo**: `.devin/skills/<nome>/SKILL.md`

```markdown
---
name: minha-skill
description: "Proposito objetivo em uma frase."
argument-hint: "[arquivo] [opcoes]"
model: sonnet               # opcional — override do modelo
subagent: true              # opcional — roda em subagente isolado
agent: security-reviewer    # opcional — usa um subagente custom especifico
allowed-tools:
  - read
  - grep
  - exec
permissions:
  allow:
    - Exec(git diff)
  deny:
    - write
triggers:
  - user                    # invocada pelo usuario (/minha-skill)
  - model                   # pode ser invocada automaticamente pelo modelo
---

# Skill: minha-skill

## Quando aplicar
- Contexto A
- Contexto B

## Processo
Passos procedurais.

## Entrada do usuario
$ARGUMENTS
```

**Invocação**: `/minha-skill argumento aqui` → `$ARGUMENTS` captura todo o input. Também disponíveis: `$1`, `$2`, etc.

**Campos do frontmatter**:

| Campo | Descrição |
|-------|-----------|
| `name` | Nome da skill (bate com a pasta) — vira o slash command |
| `description` | Aparece na paleta de autocomplete |
| `argument-hint` | Dica de uso mostrada no prompt |
| `model` | Override do modelo para essa skill |
| `subagent` | `true` roda em isolamento (contexto próprio) |
| `agent` | Nome de um subagente custom — usa o perfil dele |
| `allowed-tools` | Restringe ferramentas |
| `permissions` | Override de permissions |
| `triggers` | `user`, `model` ou ambos |

---

### 3. Nova permissão

Edite `.devin/config.json`:

```jsonc
{
  "permissions": {
    "allow": [
      "Read(src/**)",
      "Exec(meu-comando)",
      "Fetch(domain:meu-dominio.com)"
    ],
    "ask": [
      "Write(**)"
    ],
    "deny": [
      "Exec(rm -rf)"
    ]
  }
}
```

**Padrões suportados**:

| Padrão | Uso |
|--------|-----|
| `Read(<glob>)` | Read com glob (`src/**`, `**/*.java`) |
| `Write(<glob>)` | Escrita com glob |
| `Edit(<glob>)` | Edição com glob |
| `Exec(<prefix>)` | Comando shell com prefix match (`git`, `npm run`) |
| `Fetch(<pattern>)` | HTTP request (`domain:npmjs.org`) |
| `read`, `write`, `edit`, `grep`, `glob`, `exec` | Tool-level (bloqueia/libera tool inteiro) |
| `mcp__<server>__<tool>` | Ferramentas MCP |

**Precedência**: `deny` → `ask` → `allow` → default. Organização sobrescreve tudo.

Overrides pessoais (gitignored) em `.devin/config.local.json`.

---

### 4. Novo hook

Edite `.devin/config.json`, seção `hooks`:

```jsonc
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "write|edit",
        "hooks": [
          {
            "type": "command",
            "command": "bash scripts/meu-hook.sh",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```

**Eventos suportados** (7):

| Evento | Quando dispara | Payload via stdin |
|--------|---------------|-------------------|
| `SessionStart` | Início da sessão | — |
| `UserPromptSubmit` | Usuário envia mensagem | `prompt` |
| `PreToolUse` | Antes de uma tool rodar | `tool_name`, `tool_input` |
| `PostToolUse` | Depois da tool completar | `tool_name`, `tool_input`, `tool_response` |
| `PermissionRequest` | Agente precisa de aprovação | `tool_name`, `tool_input` |
| `Stop` | Agente terminou o turno | — |
| `SessionEnd` | Sessão termina | `reason` |

**Contrato**: o script recebe JSON por stdin e comunica decisão por stdout (ex: `{"decision": "block", "reason": "..."}` para bloquear em `PreToolUse`). Exit code 2 também bloqueia.

`matcher` usa regex. String vazia (`""`) casa qualquer tool.

---

### 5. Atualizar `AGENTS.md`

Toda mudança em governança (novo subagente, nova regra transversal, mudança de fluxo, nova stack) deve refletir no `AGENTS.md`. Ele é lido automaticamente pelo Devin CLI no início de cada sessão.

`AGENTS.md` é um padrão aberto reconhecido também por Copilot, Codex e outras ferramentas — manter esse arquivo consistente beneficia todas as plataformas.

---

### Checklist antes de mergear

- [ ] Arquivo no path correto (`.devin/agents/<nome>/AGENT.md` ou `.devin/skills/<nome>/SKILL.md`)?
- [ ] Frontmatter YAML válido (`name`, `description` obrigatórios)?
- [ ] Subagente registrado no `AGENTS.md` (ordem de consulta)?
- [ ] Orquestrador atualizado para conhecer o novo subagente?
- [ ] `config.json` ajustado se a nova config precisa de permissão/hook?
- [ ] Teste manual: `/minha-skill` aparece no autocomplete? Subagente é invocado corretamente?
- [ ] README atualizado com o novo papel/skill?
- [ ] Paridade avaliada com `claude-code/`, `codex/`, `copilot/`, `gemini/`?

---

## Importando configs do Claude Code (opcional)

O Devin CLI suporta auto-importar configs do Claude Code via `read_config_from`. No `config.json` deste módulo essa flag está **desativada** (`false`) porque o projeto já tem sua própria estrutura Devin completa.

Se quiser **combinar** este setup com um setup Claude Code preexistente, habilite:

```jsonc
{
  "read_config_from": {
    "claude": true
  }
}
```

O que é importado do Claude Code:
- `CLAUDE.md` (regras de projeto)
- `.claude/skills/**/SKILL.md`
- `.claude/commands/**/*.md` (convertidos para skills)
- MCP servers em `.mcp.json`, `.claude/settings.json`

**Não** é importado:
- `.claude/agents/*.md` (subagentes) — precisam ser convertidos para `.devin/agents/<nome>/AGENT.md`
- Hooks do `.claude/settings.json` — precisam ser declarados em `.devin/config.json`

---

## Referências

- [Devin CLI — Quickstart](https://cli.devin.ai/docs)
- [Devin CLI — Configuration](https://cli.devin.ai/docs/extensibility/configuration.md)
- [Devin CLI — Rules & AGENTS.md](https://cli.devin.ai/docs/extensibility/rules.md)
- [Devin CLI — Subagents](https://cli.devin.ai/docs/subagents.md)
- [Devin CLI — Skills](https://cli.devin.ai/docs/extensibility/skills/creating-skills.md)
- [Devin CLI — Lifecycle Hooks](https://cli.devin.ai/docs/extensibility/hooks/lifecycle-hooks.md)
- [Devin CLI — Permissions](https://cli.devin.ai/docs/reference/permissions.md)
- [Devin CLI — Importar de outros tools](https://cli.devin.ai/docs/reference/configuration/read-config-from.md)
