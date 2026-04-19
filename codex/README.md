# Base Enterprise Multiagente para Codex

Base desenhada para operacao profissional com Codex em repositorios de engenharia de software moderna, com foco em:
- governanca forte
- revisao multiagente
- especializacao por dominio
- seguranca, compliance, dados, performance, QA, SRE, CI/CD, custo e documentacao

## Arquitetura da solucao

A estrutura separa responsabilidades em camadas:

| Camada | Localizacao | Proposito |
|--------|-------------|-----------|
| Governanca global | `AGENTS.md` | Principios inegociaveis, fluxo de revisao, ordem de consulta |
| Configuracao do projeto | `.codex/config.toml` | Modelo padrao, sandbox, features, registro de skills |
| Agentes especializados | `.codex/agents/*.toml` | 24 perfis (nome, modelo, sandbox, instrucoes) |
| Skills/workflows | `.codex/skills/<nome>/SKILL.md` | 34 playbooks reutilizaveis |
| Hooks de lifecycle | `.codex/hooks.json` + `.codex/hooks/*.py` | Quality gates (experimental — desabilitado em Windows) |
| Templates e referencias | `.codex/templates/`, `.codex/references/` | ADR, pre-PR checklist, rubricas de severidade/tamanho/evidencia |

## Fluxo operacional recomendado

1. Entrar por `staff-engineer-orchestrator` em demanda nao trivial.
2. Rodar especialistas por risco e escopo.
3. Consolidar recomendacoes e resolver conflitos.
4. Implementar a menor mudanca correta.
5. Validar com evidencias e preparar pre-PR.

## Catalogo de agentes (24)

- `staff-engineer-orchestrator` · `dependency-versions-reviewer` · `tech-lead-reviewer` · `architect-reviewer` · `api-contract-reviewer`
- `security-reviewer` · `compliance-reviewer` · `ad-dba-reviewer` · `data-engineering-aws-architect`
- `java-specialist` · `jakarta-ee-specialist` · `python-specialist` · `go-specialist` · `frontend-specialist` · `mobile-native-specialist`
- `software-engineer` · `sre-platform-engineer` · `cicd-pipeline-engineer` · `incident-response-reviewer`
- `finops-reviewer` · `devex-reviewer` · `qa-quality-engineer` · `performance-reliability-reviewer` · `tech-writer`

## Catalogo de skills (34)

`review` · `full-review` · `implement` · `pre-pr` · `arch-review` · `security-check` · `compliance` · `contract-review` · `check-deps` · `data-review` · `data-platform` · `qa-review` · `perf-review` · `sre-review` · `cicd-review` · `finops` · `floci` · `incident-readiness` · `local-setup` · `docs` · `adr` · `changelog` · `debug` · `explain` · `health-check` · `hotfix` · `migrate` · `optimize` · `quick-fix` · `refactor` · `runbook` · `scaffold` · `tech-debt` · `test-gen`

## Decisao de design sobre skills

As skills canonicas ficam em `.codex/skills/` e sao registradas explicitamente em `[[skills.config]]` no `.codex/config.toml`. Uma skill nao registrada nao sera carregada.

## Compatibilidade de hooks no Windows

Hooks do Codex sao experimentais e, conforme documentacao oficial atual, permanecem desabilitados em runtime Windows. Os arquivos de hook sao mantidos para Linux/macOS/CI e para facilitar migracao futura.

## Estrutura final

```text
.
├─ AGENTS.md
├─ README.md
└─ .codex/
   ├─ config.toml                         # modelo, sandbox, features, registro de skills
   ├─ hooks.json                          # wiring dos hooks (Linux/macOS/CI)
   ├─ hooks/                              # scripts Python (pre_tool_use_policy, post_tool_use_review, stop_continue)
   ├─ agents/                             # 24 perfis TOML
   ├─ skills/                             # 34 skills (pasta/SKILL.md)
   ├─ templates/                          # adr-template.md, pre-pr-checklist.md
   └─ references/                         # change-size-guidelines, evidence-rules, review-severity-matrix
```

---

## Como adicionar novas configuracoes

Todos os pontos de extensao do Codex neste projeto.

### 1. Novo agente

**Arquivo**: `.codex/agents/<nome-do-agente>.toml`

```toml
name = "meu-novo-agente"
description = "Descricao curta e acionavel do papel."
model = "gpt-5.4"
model_reasoning_effort = "high"
sandbox_mode = "read-only"          # ou "workspace-write" quando o agente precisa editar
developer_instructions = """
Escopo:
- Atue somente como meu-novo-agente.

Quando usar:
- Cenarios concretos.

Quando nao usar:
- Casos que pertencem a outros agentes.

Limites de escopo:
- Nao assumir responsabilidades de outros agentes sem delegacao.
- Nao expandir escopo sem evidencia tecnica.

Comportamento obrigatorio:
- Produza analise objetiva com evidencias verificaveis.
- Diferencie risco critico, alto, medio e baixo.
- Sinalize lacunas de validacao explicitamente.
"""
```

**Registrar o agente**:
1. Adicionar na ordem de consulta do `staff-engineer-orchestrator.toml` (campo `developer_instructions`).
2. Atualizar a secao de orquestracao no `AGENTS.md` com o novo papel.

---

### 2. Nova skill (workflow)

**Arquivos**: `.codex/skills/<nome>/SKILL.md`

```markdown
---
name: minha-skill
description: Proposito objetivo da skill — o que ela entrega.
---

# Skill: minha-skill

## Quando dispara
- Quando o usuario solicitar explicitamente o workflow $name.
- Quando o contexto da tarefa for compativel com o objetivo.

## Quando NAO dispara
- Quando outro workflow do catalogo for mais especifico.
- Quando o escopo nao tiver relacao com o objetivo.

## Inputs esperados
- Contexto da demanda.
- Escopo/modulo alvo (quando aplicavel).
- Restricoes tecnicas e de risco.

## Saida esperada
- Diagnostico objetivo com evidencias.
- Recomendacao acionavel e priorizada.
- Plano de validacao proporcional ao risco.

## Workflow passo a passo
Acione o `staff-engineer-orchestrator` para [acao].

## Entrada do usuario
$ARGUMENTS

## Criterios de qualidade
- Evidencias explicitas (arquivos, simbolos, comandos, testes).
- Riscos classificados por severidade.
- Escopo controlado e sem refatoracao lateral.

## Regras de protecao
- Preferir menor mudanca defensavel.
- Nao inferir versoes por memoria quando houver dependencias.
- Nao omitir limitacoes de validacao.
```

**Registrar a skill** em `.codex/config.toml`:

```toml
[[skills.config]]
path = "./.codex/skills/minha-skill/SKILL.md"
enabled = true
```

Sem esse registro a skill nao e carregada pelo Codex.

---

### 3. Novo template ou referencia

- Templates reutilizaveis (ADR, pre-PR, runbook): `.codex/templates/<nome>.md`
- Rubricas e politicas transversais: `.codex/references/<nome>.md`

Sao referenciados pelas skills via `@include` ou citados no `developer_instructions` do agente que deve segui-los.

---

### 4. Novo hook (Linux/macOS/CI — experimental)

Os scripts Python ficam em `.codex/hooks/` e o wiring em `.codex/hooks.json`.

Estrutura tipica do `hooks.json`:

```json
{
  "version": 1,
  "hooks": {
    "preToolUse": ["./.codex/hooks/pre_tool_use_policy.py"],
    "postToolUse": ["./.codex/hooks/post_tool_use_review.py"],
    "stop": ["./.codex/hooks/stop_continue.py"]
  }
}
```

Para adicionar um novo hook:
1. Crie o script em `.codex/hooks/<nome>.py` com o contrato esperado pelo runtime Codex (stdin = payload JSON, stdout = decisao).
2. Registre o caminho no array correspondente em `.codex/hooks.json`.
3. Lembre-se: hooks nao executam em Windows — mantenha validacao alternativa em CI.

---

### 5. Ajustar ferramentas, sandbox e features

Edite `.codex/config.toml`:

```toml
# Modelo padrao, sandbox e aprovacao
model = "gpt-5.4"
sandbox_mode = "workspace-write"       # "read-only", "workspace-write" ou "danger-full-access"
approval_policy = "on-request"

[features]
codex_hooks = true                     # habilita hooks (experimental)
unified_exec = true
shell_tool = true

[agents]
max_threads = 6
max_depth = 1
job_max_runtime_seconds = 2400

[sandbox_workspace_write]
network_access = false
writable_roots = ["."]
```

Para agentes que precisam de escopo diferente (ex.: `software-engineer` que escreve codigo), defina `sandbox_mode` no proprio `.codex/agents/<nome>.toml`.

---

### 6. Atualizar o AGENTS.md

Toda mudanca em governanca (novo papel, nova regra transversal, mudanca de fluxo) deve refletir no `AGENTS.md`. Ele e o ponto de entrada que o Codex le primeiro.

---

### Checklist antes de mergear

- [ ] Agente/skill registrada no `AGENTS.md` (governanca)?
- [ ] Skill registrada em `[[skills.config]]` no `.codex/config.toml`?
- [ ] Ordem de consulta do `staff-engineer-orchestrator` atualizada?
- [ ] Hooks novos testados em Linux/macOS/CI (ja que Windows esta desabilitado)?
- [ ] Sandbox mode adequado ao agente (read-only por padrao para revisores)?
- [ ] README atualizado com o novo papel/skill?
- [ ] Paridade com as outras plataformas (`claude-code/`, `copilot/`, `gemini/`)?
