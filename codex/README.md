# Multi-Agent Orchestration para Codex

## O que e isso?

Uma estrutura de **orquestracao multiagente** para o [OpenAI Codex](https://openai.com/index/openai-codex/) que simula um **time de engenharia completo** operando via `AGENTS.md` e skills reutilizaveis.

Em vez de um unico agente fazendo tudo, voce tem **10 skills especializadas** — cada uma com papel, escopo, checklist e formato de saida definidos — coordenadas por um **orquestrador principal** (o `staff-engineer-orchestrator`) que funciona como maestro.

---

## Como funciona no Codex

O Codex opera via arquivos de instrucao persistentes no repositorio:

| Arquivo | Funcao |
|---------|--------|
| `AGENTS.md` | Documento de governanca lido automaticamente pelo Codex. Define stack, regras, checklists e ordem de consulta. |
| `codex/skills/*/SKILL.md` | Cada skill define um papel especializado com escopo, regras e formato de saida. |

### Diferenca para Claude Code

| Aspecto | Claude Code | Codex |
|---------|------------|-------|
| Instrucoes globais | `CLAUDE.md` | `AGENTS.md` |
| Agentes/skills | `.claude/agents/*.md` (frontmatter YAML) | `codex/skills/*/SKILL.md` (metadata em texto) |
| Configuracao | `.claude/settings.json` | `AGENTS.md` (inline) |
| Invocacao de sub-agentes | `Agent(...)` tool nativa | Leitura sequencial das skills pelo orquestrador |
| Modelo por agente | Configuravel no frontmatter | Definido pelo runtime do Codex |

---

## Estrutura do repositorio

```
codex/
├── AGENTS.md                                           # Governanca do projeto
├── README.md                                           # Este arquivo
└── skills/
    ├── staff-engineer-orchestrator/SKILL.md             # Maestro principal
    ├── tech-lead-reviewer/SKILL.md                      # Pragmatismo e manutenibilidade
    ├── architect-reviewer/SKILL.md                      # Arquitetura e boundaries
    ├── api-contract-reviewer/SKILL.md                   # Contratos de borda e schema governance
    ├── security-reviewer/SKILL.md                       # Seguranca e hardening
    ├── ad-dba-reviewer/SKILL.md                         # Dados e persistencia
    ├── software-engineer/SKILL.md                       # Implementacao
    ├── sre-platform-engineer/SKILL.md                   # Operabilidade e plataforma
    ├── qa-quality-engineer/SKILL.md                     # Testes e qualidade
    └── performance-reliability-reviewer/SKILL.md        # Performance e confiabilidade
```

---

## Skills disponiveis

| # | Skill | Papel |
|---|-------|-------|
| 0 | `staff-engineer-orchestrator` | Maestro — coordena, consolida, resolve conflitos, entrega plano final (16 secoes) |
| 1 | `tech-lead-reviewer` | Pragmatismo, simplicidade, custo de manutencao |
| 2 | `architect-reviewer` | Boundaries, acoplamento, resiliencia, contratos |
| 3 | `api-contract-reviewer` | Contratos de borda (OpenAPI, Protobuf, GraphQL, Avro, AsyncAPI) |
| 4 | `security-reviewer` | Seguranca, hardening, superficies de abuso |
| 5 | `ad-dba-reviewer` | Dados, modelagem, queries, indices, CAP theorem |
| 6 | `software-engineer` | Implementacao minima correta |
| 7 | `sre-platform-engineer` | Operabilidade, deploy, observabilidade, IaC |
| 8 | `qa-quality-engineer` | Testes (JUnit 5, PIT, ArchUnit, Testcontainers), edge cases |
| 9 | `performance-reliability-reviewer` | Throughput, latencia, escalabilidade |

---

## Ordem de consulta

O orquestrador segue esta ordem preferencial:

1. tech-lead-reviewer
2. architect-reviewer
3. api-contract-reviewer
4. security-reviewer
5. ad-dba-reviewer
6. software-engineer
7. sre-platform-engineer
8. qa-quality-engineer
9. performance-reliability-reviewer

---

## Como usar

### No Codex

1. O Codex le `AGENTS.md` automaticamente ao operar neste repositorio
2. Para demandas nao triviais, instrua o Codex a seguir o papel de `staff-engineer-orchestrator`
3. O orquestrador aplica cada skill relevante e consolida a resposta

### Uso direto de uma skill

Para analise focada, instrua o Codex a seguir uma skill especifica:

```
Siga as instrucoes de codex/skills/security-reviewer/SKILL.md
e revise a configuracao de autenticacao do endpoint /api/v1/payments
```

---

## Como criar uma nova skill

### 1. Crie o diretorio e arquivo

```bash
mkdir -p codex/skills/minha-nova-skill
touch codex/skills/minha-nova-skill/SKILL.md
```

### 2. Escreva o SKILL.md

```markdown
# Nome da Skill

**name:** minha-nova-skill
**description:** Descricao curta e objetiva.

---

## Papel
O que essa skill faz.

## Escopo de revisao
- Item 1
- Item 2

## Regras mandatorias
- Regra 1
- Regra 2

## Checklist de revisao
- [ ] Check 1?
- [ ] Check 2?

## Formato de saida obrigatorio

### 1. Secao 1
Descricao.

### 2. Secao 2
Descricao.
```

### 3. Registre no orquestrador e no AGENTS.md (se necessario)

Adicione a nova skill na ordem de consulta do `staff-engineer-orchestrator/SKILL.md` e na lista do `AGENTS.md`.

---

## Portabilidade

Esta estrutura e **agnositca ao nome do projeto**. Para usar em outro repositorio:

1. Copie `AGENTS.md` e a pasta `codex/skills/` para o novo repo
2. Adapte stack e regras no `AGENTS.md`
3. Ajuste as skills conforme necessario

Os placeholders `<project-root>/` e `<base-package>/` facilitam o reuso.
