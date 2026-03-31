# Multi-Agent Governance para Codex

## Estado real do modulo

Este repositorio **nao contem uma aplicacao Java executavel** (nao ha `src/`, `pom.xml`, `build.gradle` ou pipeline de build).

O modulo atual e um **kit de governanca multiagente** para o Codex, composto por:

- `AGENTS.md`: regras globais do projeto (papel padrao, stack-alvo, checklists e disciplina operacional).
- `.agents/skills/*/SKILL.md`: definicao das skills especializadas.
- `.codex/config.toml` e `.codex/agents/*.toml`: configuracao de agentes do runtime (modelo, sandbox e instrucoes).

## Estrutura atual do repositorio

```text
.
├── AGENTS.md
├── README.md
├── .agents/
│   └── skills/
│       ├── staff-engineer-orchestrator/SKILL.md
│       ├── tech-lead-reviewer/SKILL.md
│       ├── architect-reviewer/SKILL.md
│       ├── api-contract-reviewer/SKILL.md
│       ├── security-reviewer/SKILL.md
│       ├── ad-dba-reviewer/SKILL.md
│       ├── software-engineer/SKILL.md
│       ├── sre-platform-engineer/SKILL.md
│       ├── qa-quality-engineer/SKILL.md
│       └── performance-reliability-reviewer/SKILL.md
└── .codex/
    ├── config.toml
    └── agents/
        ├── staff-engineer-orchestrator.toml
        ├── tech-lead-reviewer.toml
        ├── architect-reviewer.toml
        ├── api-contract-reviewer.toml
        ├── security-reviewer.toml
        ├── ad-dba-reviewer.toml
        ├── software-engineer.toml
        ├── sre-platform-engineer.toml
        ├── qa-quality-engineer.toml
        └── performance-reliability-reviewer.toml
```

## Skills ativas

Total atual: **10 skills**.

1. `staff-engineer-orchestrator`
2. `tech-lead-reviewer`
3. `architect-reviewer`
4. `api-contract-reviewer`
5. `security-reviewer`
6. `ad-dba-reviewer`
7. `software-engineer`
8. `sre-platform-engineer`
9. `qa-quality-engineer`
10. `performance-reliability-reviewer`

## Como usar no dia a dia

1. Abra este repositorio no Codex.
2. Deixe o `AGENTS.md` guiar o comportamento global.
3. Para demanda nao trivial, inicie com o papel `staff-engineer-orchestrator`.
4. Para demanda pontual, solicite diretamente a skill especializada.

Exemplo:

```text
Siga as instrucoes de .agents/skills/security-reviewer/SKILL.md
e revise a configuracao de autenticacao do endpoint /api/v1/payments
```

## Como adicionar uma nova skill

1. Crie o arquivo da skill em `.agents/skills/<nome>/SKILL.md`.
2. Crie o agente correspondente em `.codex/agents/<nome>.toml`.
3. Atualize a ordem de consulta no `AGENTS.md` e no `staff-engineer-orchestrator/SKILL.md` quando necessario.

## Notas de compatibilidade

- O modulo ja usa a estrutura nova (`.agents/skills` + `.codex/agents`).
- Se encontrar referencia textual a `codex/skills/`, trate como **legado** e use `.agents/skills/`.
- A stack de Java/AWS descrita no `AGENTS.md` e **contexto-alvo para projetos consumidores**, nao um codigo implementado neste repositorio.
