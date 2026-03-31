# Multi-Agents

Estrutura multiagente para diferentes plataformas de AI coding assistants.

Cada pasta contem a estrutura completa e pronta para uso da plataforma correspondente, com os mesmos 10 papeis especializados adaptados ao modelo operacional de cada ferramenta.

```
.
├── claude-code/          # Claude Code — CLAUDE.md + .claude/agents/*.md
│   ├── CLAUDE.md
│   └── .claude/agents/
├── codex/                # OpenAI Codex — AGENTS.md + .agents/skills/*/SKILL.md + .codex/agents/*.toml
│   ├── AGENTS.md
│   ├── .agents/skills/
│   └── .codex/agents/
├── copilot/              # GitHub Copilot — AGENTS.md + .github/agents/*.agent.md + .github/instructions/ + docs/ai/
│   ├── AGENTS.md
│   ├── .github/
│   │   ├── copilot-instructions.md
│   │   ├── agents/
│   │   └── instructions/
│   └── docs/ai/
└── gemini/               # Google Gemini CLI — GEMINI.md + .gemini/commands/*.toml + docs/ai/
    ├── GEMINI.md
    ├── .gemini/
    │   ├── settings.json
    │   └── commands/
    └── docs/ai/
```

## Papeis (consistentes entre plataformas)

| # | Papel | Foco |
|---|-------|------|
| 0 | staff-engineer-orchestrator | Maestro — coordena, consolida, plano final |
| 1 | tech-lead-reviewer | Pragmatismo, simplicidade, manutencao |
| 2 | architect-reviewer | Boundaries, resiliencia, contratos |
| 3 | api-contract-reviewer | OpenAPI, Protobuf, GraphQL, Avro, AsyncAPI |
| 4 | security-reviewer | Seguranca, hardening |
| 5 | ad-dba-reviewer | Dados, modelagem, queries |
| 6 | software-engineer | Implementacao minima correta |
| 7 | sre-platform-engineer | Operabilidade, IaC |
| 8 | qa-quality-engineer | Testes, edge cases |
| 9 | performance-reliability-reviewer | Throughput, latencia |

## Comparativo entre plataformas

| Aspecto | Claude Code | Codex | Copilot | Gemini |
|---------|------------|-------|---------|--------|
| Instrucoes globais | `CLAUDE.md` | `AGENTS.md` | `AGENTS.md` + `.github/copilot-instructions.md` | `GEMINI.md` |
| Agentes/roles | `.claude/agents/*.md` | `.agents/skills/*/SKILL.md` + `.codex/agents/*.toml` | `.github/agents/*.agent.md` + `docs/ai/roles/*.md` | `.gemini/commands/*.toml` + `docs/ai/roles/*.md` |
| Sub-agentes | `Agent(...)` nativo | Leitura sequencial por prompt | Instrucao de prompt | Comandos `/role` no terminal |
| Modelo por agente | Frontmatter YAML (`opus`/`sonnet`/`haiku`) | Runtime (`.codex/agents/*.toml`) | Nao configuravel | Nao configuravel |
| Orquestracao | Automatica | Semi-automatica | Manual via prompt | Manual via `/comando` |

## Mecanismo de invocacao por plataforma

| Plataforma | Como acionar agentes |
|-----------|---------------------|
| **Claude Code** | Orquestracao nativa via `Agent(...)` — o orquestrador invoca sub-agentes automaticamente |
| **Codex** | Semi-automatica — o prompt referencia o `SKILL.md` e solicita consulta sequencial |
| **Copilot** | Manual — seletor de agentes no painel Copilot Chat (VS Code, modo Agent) ou por instrucao no prompt |
| **Gemini** | Manual — comandos `/role` no terminal (ex.: `/security-reviewer`, `/architect-reviewer`) |

Consulte o README de cada pasta para instrucoes detalhadas de uso.
