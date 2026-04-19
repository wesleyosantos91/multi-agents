# Multi-Agents

Estrutura multiagente para diferentes plataformas de AI coding assistants.

Cada pasta contem a estrutura completa e pronta para uso da plataforma correspondente, com os mesmos **24 papeis especializados** adaptados ao modelo operacional de cada ferramenta.

```
.
├── claude-code/          # Claude Code — CLAUDE.md + .claude/{agents,commands,skills} + settings.json
│   ├── CLAUDE.md
│   ├── README.md
│   └── .claude/
│       ├── settings.json
│       ├── agents/              # 24 agentes (Markdown + frontmatter YAML)
│       ├── commands/            # 33 slash commands
│       └── skills/              # 46 skills locais
├── codex/                # OpenAI Codex — AGENTS.md + .codex/{agents,skills,hooks,templates,references}
│   ├── AGENTS.md
│   ├── README.md
│   └── .codex/
│       ├── config.toml
│       ├── hooks.json
│       ├── hooks/               # scripts Python (Linux/macOS/CI)
│       ├── agents/              # 24 agentes (.toml)
│       ├── skills/              # 34 skills (pasta/SKILL.md)
│       ├── templates/           # templates reutilizaveis (ADR, pre-PR)
│       └── references/          # rubricas de severidade, tamanho, evidencia
├── copilot/              # GitHub Copilot — AGENTS.md + .github/{agents,instructions,prompts,skills,knowledge,hooks}
│   ├── AGENTS.md
│   ├── README.md
│   └── .github/
│       ├── copilot-instructions.md
│       ├── copilot/settings.json
│       ├── agents/              # 24 agentes (.agent.md)
│       ├── instructions/        # 19 instrucoes contextuais (applyTo)
│       ├── prompts/             # 34 prompts reutilizaveis
│       ├── skills/              # 45 skills
│       ├── knowledge/           # playbooks detalhados por papel + docs-reference
│       └── hooks/               # quality-gates + scripts PowerShell
├── gemini/               # Google Gemini CLI — GEMINI.md + .gemini/{agents,commands,skills}
│   ├── GEMINI.md
│   ├── README.md
│   └── .gemini/
│       ├── settings.json
│       ├── agents/              # 24 agentes (Markdown)
│       ├── commands/            # 58 comandos TOML (orchestrate, reviews, roles, workflows)
│       └── skills/              # 46 skills
└── devin/                # Devin CLI — AGENTS.md + .devin/{agents,skills} + config.json
    ├── AGENTS.md
    ├── README.md
    └── .devin/
        ├── config.json          # permissoes, hooks, read_config_from
        ├── agents/              # 24 subagentes (pasta/AGENT.md + frontmatter YAML)
        └── skills/              # 79 skills (slash commands + conhecimento procedural)
```

## Papeis (consistentes entre plataformas)

| # | Papel | Foco |
|---|-------|------|
| 0 | staff-engineer-orchestrator | Maestro — coordena, consolida, plano final |
| 1 | dependency-versions-reviewer | Versoes GA via WebSearch — Java, Python, Go, AWS runtimes |
| 2 | tech-lead-reviewer | Pragmatismo, simplicidade, manutencao |
| 3 | architect-reviewer | Boundaries, resiliencia, contratos |
| 4 | api-contract-reviewer | OpenAPI, Protobuf, GraphQL, Avro, AsyncAPI |
| 5 | security-reviewer | Seguranca, hardening (Java, Python, Go, serverless) |
| 6 | compliance-reviewer | LGPD, GDPR, residencia de dados, serverless compliance |
| 7 | ad-dba-reviewer | Dados, modelagem, queries |
| 8 | data-engineering-aws-architect | Pipelines, Glue, EMR, Kinesis, Athena |
| 9 | java-specialist | Java 25, Spring Boot, Quarkus, Micronaut |
| 10 | jakarta-ee-specialist | Jakarta EE 11, MicroProfile 7.0, WildFly, Open Liberty |
| 11 | python-specialist | Python, pyproject.toml, pytest, Ruff, Lambda Python |
| 12 | go-specialist | Go, go.mod, interfaces, context, table-driven tests |
| 13 | frontend-specialist | React (Vite+TS), Angular (Standalone+Signals), AngularJS |
| 14 | mobile-native-specialist | Android (Kotlin+Compose), iOS (Swift+SwiftUI) |
| 15 | software-engineer | Implementacao minima correta (poliglota) |
| 16 | sre-platform-engineer | Operabilidade, IaC, Lambda observability |
| 17 | cicd-pipeline-engineer | GitHub Actions, deploy Lambda, rollback |
| 18 | incident-response-reviewer | SLOs/SLIs, runbooks, chaos engineering |
| 19 | finops-reviewer | Custo AWS, rightsizing, anti-padroes de billing |
| 20 | devex-reviewer | Onboarding, ambiente local, Dev Container |
| 21 | qa-quality-engineer | Testes, edge cases, regressoes |
| 22 | performance-reliability-reviewer | Throughput, latencia, cold start |
| 23 | tech-writer | README, getting-started, testing, troubleshooting, ADRs |

## Comparativo entre plataformas

| Aspecto | Claude Code | Codex | Copilot | Gemini | Devin |
|---------|------------|-------|---------|--------|-------|
| Instrucoes globais | `CLAUDE.md` | `AGENTS.md` | `AGENTS.md` + `.github/copilot-instructions.md` | `GEMINI.md` | `AGENTS.md` |
| Formato dos agentes | Markdown + frontmatter YAML | TOML (`.codex/agents/*.toml`) | `.agent.md` (frontmatter YAML) | Markdown puro | `AGENT.md` (frontmatter YAML) |
| Comandos/workflows | `.claude/commands/*.md` (33) | `.codex/skills/*/SKILL.md` (34) | `.github/prompts/*.prompt.md` (34) | `.gemini/commands/**/*.toml` (58) | `.devin/skills/*/SKILL.md` (79)* |
| Skills reutilizaveis | `.claude/skills/` (46) | Skills fazem papel duplo | `.github/skills/` (45) | `.gemini/skills/` (46) | Merged com commands (no campo `skills/`) |
| Sub-agentes | `Agent(...)` nativo | Delegacao em `.codex/config.toml` | Instrucao via prompt | Comandos `/role` | `subagent: true` ou `agent: <nome>` em skills |
| Modelo por agente | Frontmatter YAML (`opus`/`sonnet`/`haiku`) | `.codex/agents/*.toml` | Nao configuravel | Nao configuravel | Frontmatter YAML (`model:`) |
| Hooks | `.claude/settings.json` (bash) | `.codex/hooks/*.py` (exp. Linux/macOS) | `.github/hooks/*.ps1` | `.gemini/settings.json` (powershell) | `.devin/config.json` (7 eventos, bash) |
| Orquestracao | Automatica | Semi-automatica | Manual via prompt | Manual via `/comando` | Via subagents (foreground/background) |

\* Devin combina slash commands e skills reutilizaveis em um unico catalogo `skills/`, invocados por `/<nome>`.

## Mecanismo de invocacao por plataforma

| Plataforma | Como acionar agentes |
|-----------|---------------------|
| **Claude Code** | Orquestracao nativa via `Agent(...)` — o orquestrador invoca sub-agentes automaticamente |
| **Codex** | Semi-automatica — o prompt referencia o `SKILL.md` e solicita consulta sequencial |
| **Copilot** | Manual — seletor de agentes no painel Copilot Chat (VS Code, modo Agent) ou por instrucao no prompt |
| **Gemini** | Manual — comandos `/role` no terminal (ex.: `/security-reviewer`, `/architect-reviewer`) |
| **Devin** | Subagentes isolados — invocados pelo agente principal via `subagent: true` / `agent: <nome>` ou `/skill` |

---

## Como adicionar novas configuracoes (resumo cross-plataforma)

Cada plataforma tem seu formato, mas a ideia e a mesma: criar o arquivo, registrar na governanca (CLAUDE.md/AGENTS.md/GEMINI.md) e, quando aplicavel, atualizar a ordem de consulta do orquestrador. O detalhe especifico de cada plataforma esta no README de cada pasta.

| Adicao | Claude Code | Codex | Copilot | Gemini | Devin |
|--------|-------------|-------|---------|--------|-------|
| Novo agente | `.claude/agents/<nome>.md` com frontmatter YAML | `.codex/agents/<nome>.toml` | `.github/agents/<nome>.agent.md` + playbook em `.github/knowledge/agents/<nome>.md` | `.gemini/agents/<nome>.md` + `.gemini/commands/roles/<nome>.toml` | `.devin/agents/<nome>/AGENT.md` com frontmatter YAML |
| Novo comando/workflow | `.claude/commands/<nome>.md` | `.codex/skills/<nome>/SKILL.md` + registro em `.codex/config.toml` (`[[skills.config]]`) | `.github/prompts/<nome>.prompt.md` | `.gemini/commands/<categoria>/<nome>.toml` | `.devin/skills/<nome>/SKILL.md` (invocado via `/<nome>`) |
| Nova skill/conhecimento | `.claude/skills/<nome>/SKILL.md` | `.codex/skills/<nome>/SKILL.md` (mesmo arquivo do workflow) | `.github/skills/<nome>/SKILL.md` | `.gemini/skills/<nome>/SKILL.md` | `.devin/skills/<nome>/SKILL.md` (mesmo arquivo do command) |
| Nova instrucao contextual | Ajuste no `CLAUDE.md` | Ajuste no `AGENTS.md` | `.github/instructions/<nome>.instructions.md` com `applyTo` | Ajuste no `GEMINI.md` | Ajuste no `AGENTS.md` (ou `AGENTS.md` aninhado em subdiretorio) |
| Hook adicional | Editar `.claude/settings.json` (`PreToolUse`/`PostToolUse`) | Editar `.codex/hooks.json` + script em `.codex/hooks/` | Editar `.github/hooks/quality-gates.json` + script em `.github/hooks/scripts/` | Editar `.gemini/settings.json` (`BeforeTool`/`AfterTool`) | Editar `.devin/config.json` (7 eventos: SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, PermissionRequest, Stop, SessionEnd) |
| Permissao/ferramenta | `.claude/settings.json` (`permissions.allow` / `permissions.deny`) | `.codex/config.toml` (`sandbox_mode`, `sandbox_workspace_write`) | `.github/copilot/settings.json` | `.gemini/settings.json` (`tools.allowed`) | `.devin/config.json` (`permissions.allow` / `ask` / `deny` com `Read/Write/Edit/Exec/Fetch(<pattern>)`) |
| Registrar no orquestrador | `staff-engineer-orchestrator.md` (ordem de consulta) + `CLAUDE.md` | `.codex/agents/staff-engineer-orchestrator.toml` + `AGENTS.md` | `.github/knowledge/agents/staff-engineer-orchestrator.md` + `AGENTS.md` | `.gemini/agents/staff-engineer-orchestrator.md` + `GEMINI.md` | `.devin/agents/staff-engineer-orchestrator/AGENT.md` + `AGENTS.md` |

### Checklist antes de mergear uma nova config

1. O novo agente/comando/skill aparece na governanca (`CLAUDE.md` / `AGENTS.md` / `GEMINI.md`)?
2. A ordem de consulta do `staff-engineer-orchestrator` foi atualizada quando o papel precisa participar de revisoes?
3. O README da plataforma foi atualizado (nomes, contagens, proposito)?
4. Se for agente poliglota, as outras plataformas receberam o mesmo papel? (paridade entre as 5 pastas)
5. Se adiciona hook ou permissao, ha teste/validacao manual documentada?

Consulte o README de cada pasta para o passo a passo completo da plataforma correspondente.
