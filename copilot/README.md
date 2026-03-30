# Multi-Agent Orchestration para GitHub Copilot

## O que e isso?

Uma estrutura de **orquestracao por papeis virtuais** para o [GitHub Copilot](https://github.com/features/copilot) que simula um **time de engenharia completo** via documentacao versionada no repositorio.

Em vez de um unico prompt generico, voce tem **10 papeis especializados** documentados — cada um com escopo, regras, checklist e formato de saida — coordenados por um **orquestrador** (`staff-engineer-orchestrator`).

---

## Como funciona no Copilot

O GitHub Copilot nao tem sub-agentes nativos como Claude Code ou skills como Codex. A orquestracao e feita por **instrucoes versionadas** que voce referencia no prompt:

| Arquivo | Funcao |
|---------|--------|
| `.github/copilot-instructions.md` | Instrucoes globais lidas automaticamente pelo Copilot |
| `docs/ai/orchestration/*.md` | Orquestrador principal |
| `docs/ai/roles/*.md` | Papeis especializados |

### Diferenca entre plataformas

| Aspecto | Claude Code | Codex | Copilot |
|---------|------------|-------|---------|
| Instrucoes globais | `CLAUDE.md` | `AGENTS.md` | `.github/copilot-instructions.md` |
| Agentes/roles | `.claude/agents/*.md` | `codex/skills/*/SKILL.md` | `docs/ai/roles/*.md` |
| Sub-agentes | `Agent(...)` nativo | Leitura sequencial | Referencia no prompt |
| Modelo por agente | Frontmatter YAML | Runtime do Codex | Nao configuravel |
| Orquestracao | Automatica | Semi-automatica | Manual via prompt |

---

## Estrutura

```
copilot/
├── .github/
│   └── copilot-instructions.md                        # Instrucoes globais
├── docs/ai/
│   ├── orchestration/
│   │   └── staff-engineer-orchestrator.md              # Maestro principal
│   └── roles/
│       ├── tech-lead-reviewer.md                       # Pragmatismo
│       ├── architect-reviewer.md                       # Arquitetura
│       ├── api-contract-reviewer.md                    # Contratos de borda
│       ├── security-reviewer.md                        # Seguranca
│       ├── ad-dba-reviewer.md                          # Dados
│       ├── software-engineer.md                        # Implementacao
│       ├── sre-platform-engineer.md                    # Operabilidade
│       ├── qa-quality-engineer.md                      # Testes
│       └── performance-reliability-reviewer.md         # Performance
└── README.md
```

---

## Papeis disponiveis

| # | Papel | Foco |
|---|-------|------|
| 0 | `staff-engineer-orchestrator` | Maestro — coordena, consolida, plano final (16 secoes) |
| 1 | `tech-lead-reviewer` | Pragmatismo, simplicidade |
| 2 | `architect-reviewer` | Boundaries, resiliencia, contratos |
| 3 | `api-contract-reviewer` | OpenAPI, Protobuf, GraphQL, Avro, AsyncAPI |
| 4 | `security-reviewer` | Seguranca, hardening |
| 5 | `ad-dba-reviewer` | Dados, modelagem, queries |
| 6 | `software-engineer` | Implementacao minima |
| 7 | `sre-platform-engineer` | Operabilidade, IaC |
| 8 | `qa-quality-engineer` | Testes, edge cases |
| 9 | `performance-reliability-reviewer` | Throughput, latencia |

---

## Como usar

### Orquestracao completa (demanda nao trivial)

Cole no prompt do Copilot:

```
Siga as instrucoes de docs/ai/orchestration/staff-engineer-orchestrator.md
como papel principal. Consulte os papeis em docs/ai/roles/ conforme a ordem
definida em .github/copilot-instructions.md. Consolide a resposta no formato
de saida obrigatorio do orquestrador (16 secoes).

Demanda: Preciso adicionar um endpoint REST para consulta de pedidos
com paginacao, filtro por status e ordenacao por data.
```

### Analise focada (papel especifico)

```
Siga as instrucoes de docs/ai/roles/security-reviewer.md e revise
a configuracao de autenticacao do endpoint /api/v1/payments.
```

### Implementacao direta (tarefa trivial)

```
Siga as instrucoes de docs/ai/roles/software-engineer.md e corrija
o typo no campo "stauts" para "status" na entity Order.
```

---

## Como criar um novo papel

### 1. Crie o arquivo

```bash
touch docs/ai/roles/meu-novo-papel.md
```

### 2. Escreva o conteudo

```markdown
# Nome do Papel

**Papel:** Descricao curta.

---

## Escopo de revisao
- Item 1
- Item 2

## Regras mandatorias
- Regra 1
- Regra 2

## Checklist
- [ ] Check 1?
- [ ] Check 2?

## Formato de saida obrigatorio
### 1. Secao 1
### 2. Secao 2
```

### 3. Registre no orquestrador e nas instrucoes globais

Adicione na ordem de consulta do `staff-engineer-orchestrator.md` e no `.github/copilot-instructions.md`.

---

## Portabilidade

Para usar em outro repositorio:

1. Copie `.github/copilot-instructions.md` e `docs/ai/` para o novo repo
2. Adapte stack e regras
3. Ajuste papeis conforme necessario

Placeholders `<project-root>/` e `<base-package>/` facilitam o reuso.
