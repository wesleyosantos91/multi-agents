# Multi-Agents

Estrutura multiagente para diferentes plataformas de AI coding assistants.

Cada pasta contem a estrutura completa e pronta para uso da plataforma correspondente, com os mesmos 10 papeis especializados adaptados ao modelo operacional de cada ferramenta.

```
.
├── claude-code/   # Claude Code — .claude/agents/*.md + CLAUDE.md
├── codex/         # OpenAI Codex — skills/*/SKILL.md + AGENTS.md
├── copilot/       # GitHub Copilot — docs/ai/roles/*.md + .github/copilot-instructions.md
└── gemini/        # Google Gemini — docs/ai/roles/*.md + docs/ai/gemini-instructions.md
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
| Instrucoes globais | `CLAUDE.md` | `AGENTS.md` | `.github/copilot-instructions.md` | `docs/ai/gemini-instructions.md` |
| Agentes/roles | `.claude/agents/*.md` | `skills/*/SKILL.md` | `docs/ai/roles/*.md` | `docs/ai/roles/*.md` |
| Sub-agentes | `Agent(...)` nativo | Leitura sequencial | Referencia no prompt | Referencia no prompt |
| Modelo por agente | Frontmatter YAML | Runtime | Nao configuravel | Nao configuravel |
| Orquestracao | Automatica | Semi-automatica | Manual via prompt | Manual via prompt |

Consulte o README de cada pasta para instrucoes detalhadas de uso.
