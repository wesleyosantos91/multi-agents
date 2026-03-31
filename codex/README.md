# Multi-Agent Governance para Codex

## O que este repositorio e

Este repositorio **nao contem uma aplicacao Java executavel** (nao ha `src/`, `pom.xml`, `build.gradle` ou pipeline de build).

Ele e um **kit de governanca multiagente** para o Codex, composto por:

- `AGENTS.md`: regras globais do projeto (papel padrao, stack-alvo, checklists e disciplina operacional).
- `.agents/skills/*/SKILL.md`: definicao de cada skill especializada.
- `.codex/config.toml` e `.codex/agents/*.toml`: configuracao de runtime dos agentes (modelo, sandbox e instrucoes).

## Estrutura atual

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

## Como utilizar multiagents no dia a dia

### Fluxo recomendado (demanda nao trivial)

1. Passe o contexto completo da demanda.
2. Inicie pelo `staff-engineer-orchestrator`.
3. Exija consulta das skills relevantes antes de implementar.
4. Implemente somente apos plano consolidado.

Exemplo de prompt:

```text
Atue como staff-engineer-orchestrator seguindo AGENTS.md.

Demanda:
- Revisar e propor mudancas para resiliencia e observabilidade do fluxo de pagamentos.

Requisitos:
- Consultar skills na ordem definida em AGENTS.md.
- Separar risco critico de melhoria futura.
- Entregar plano final priorizado.
- So depois propor implementacao minima segura.
```

### Fluxo direto (demanda pontual)

Para atividade pequena e localizada, acione uma skill especifica:

```text
Siga as instrucoes de .agents/skills/security-reviewer/SKILL.md
e revise a configuracao de autenticacao do endpoint /api/v1/payments
```

### Fluxo de implementacao apos analise

Depois do plano consolidado, direcione implementacao minima:

```text
Com base no plano consolidado, atue como software-engineer e implemente
apenas a menor mudanca correta, preservando backward compatibility.
Liste arquivos alterados, riscos remanescentes e comandos de validacao.
```

## Verificacao rapida (se esta "certinho")

Use estes comandos no PowerShell para validar estrutura e consistencia:

```powershell
Get-ChildItem .agents/skills -Directory | Select-Object -ExpandProperty Name
Get-ChildItem .codex/agents/*.toml | Select-Object -ExpandProperty Name
Get-Content .codex/config.toml
```

Se os nomes de skills em `.agents/skills` e `.codex/agents` estiverem alinhados, a base multiagente esta consistente.

## Como adicionar uma nova skill

1. Crie o arquivo em `.agents/skills/<nome>/SKILL.md`.
2. Crie o agente correspondente em `.codex/agents/<nome>.toml`.
3. Atualize a ordem de consulta no `AGENTS.md` e no `staff-engineer-orchestrator/SKILL.md` quando necessario.

## Notas de compatibilidade

- O repositorio usa a estrutura atual (`.agents/skills` + `.codex/agents`).
- Se encontrar referencia textual a `codex/skills/`, trate como **legado** e use `.agents/skills/`.
- A stack Java/AWS no `AGENTS.md` e **contexto-alvo para projetos consumidores**, nao codigo executavel neste repositorio.
