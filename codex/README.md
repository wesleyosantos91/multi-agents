# Multi-Agent Governance para Codex

## O que este repositorio e

Este repositorio **nao contem uma aplicacao Java executavel** (nao ha `src/`, `pom.xml`, `build.gradle` ou pipeline de build).

Ele e um **kit de governanca multiagente** para o Codex, composto por:

- `AGENTS.md`: regras globais do projeto (papel padrao, stack-alvo, checklists e disciplina operacional).
- `.agents/skills/*/SKILL.md`: definicao de cada skill especializada (papel, escopo, regras, checklist, formato de saida).
- `.codex/config.toml` e `.codex/agents/*.toml`: configuracao de runtime dos agentes (modelo, sandbox e instrucoes).

---

## Por que usar?

### O problema

Quando voce usa um unico agente de IA para tarefas complexas:

- Ele tenta resolver tudo de uma vez, sem analise adequada
- Perde perspectivas importantes (seguranca, performance, operabilidade)
- Nao diferencia risco critico de melhoria futura
- Nao considera trade-offs sob multiplas perspectivas
- Tende a overengineering ou a solucoes incompletas

### A solucao

Com multiagentes, cada especialista foca no que sabe. O orquestrador garante que nenhuma perspectiva e ignorada e que a resposta final e consolidada e priorizada.

### Ganhos concretos

| Ganho | Descricao |
|-------|-----------|
| **Cobertura ampla** | 18 perspectivas especializadas em vez de uma generica |
| **Qualidade de analise** | Cada agente tem checklist e regras mandatorias do seu dominio |
| **Rastreabilidade** | Saida estruturada com secoes fixas — facil de auditar e comparar |
| **Conflitos explicitos** | Quando dois agentes discordam, o orquestrador explicita e resolve |
| **Priorizacao** | Plano final ordenado por prioridade com justificativa |
| **Riscos visiveis** | Riscos remanescentes listados explicitamente |
| **Reprodutibilidade** | Mesma estrutura de resposta toda vez, independente da demanda |
| **Escalabilidade** | Facil adicionar novos agentes sem quebrar o fluxo |

### Trade-offs

| Trade-off | Descricao |
|-----------|-----------|
| **Latencia** | Multiplos agentes = mais tempo de resposta. Para tarefas triviais, pode ser excessivo |
| **Custo de tokens** | Cada agente consome tokens. Demandas simples custam mais que o necessario |
| **Overhead para tarefas simples** | Para um bugfix pontual, acionar 9 agentes e desproporcional |
| **Orquestracao semi-automatica** | O Codex nao aciona agentes automaticamente — voce precisa referenciar a skill no prompt |

**Regra pratica**: use o orquestrador para demandas nao triviais. Para tarefas simples, acione diretamente o agente relevante.

---

## Estrutura atual

```text
.
├── AGENTS.md
├── README.md
├── .agents/
│   └── skills/
│       ├── staff-engineer-orchestrator/SKILL.md
│       ├── dependency-versions-reviewer/SKILL.md
│       ├── tech-lead-reviewer/SKILL.md
│       ├── architect-reviewer/SKILL.md
│       ├── api-contract-reviewer/SKILL.md
│       ├── security-reviewer/SKILL.md
│       ├── compliance-reviewer/SKILL.md
│       ├── ad-dba-reviewer/SKILL.md
│       ├── data-engineering-aws-architect/SKILL.md
│       ├── java-specialist/SKILL.md
│       ├── python-specialist/SKILL.md
│       ├── go-specialist/SKILL.md
│       ├── software-engineer/SKILL.md
│       ├── sre-platform-engineer/SKILL.md
│       ├── finops-reviewer/SKILL.md
│       ├── devex-reviewer/SKILL.md
│       ├── qa-quality-engineer/SKILL.md
│       ├── performance-reliability-reviewer/SKILL.md
│       └── tech-writer/SKILL.md
└── .codex/
    ├── config.toml
    └── agents/
        ├── staff-engineer-orchestrator.toml
        ├── dependency-versions-reviewer.toml
        ├── tech-lead-reviewer.toml
        ├── architect-reviewer.toml
        ├── api-contract-reviewer.toml
        ├── security-reviewer.toml
        ├── compliance-reviewer.toml
        ├── ad-dba-reviewer.toml
        ├── data-engineering-aws-architect.toml
        ├── java-specialist.toml
        ├── python-specialist.toml
        ├── go-specialist.toml
        ├── software-engineer.toml
        ├── sre-platform-engineer.toml
        ├── finops-reviewer.toml
        ├── devex-reviewer.toml
        ├── qa-quality-engineer.toml
        ├── performance-reliability-reviewer.toml
        └── tech-writer.toml
```

---

## Agentes disponíveis

Total atual: **19 skills**.

| # | Skill | Foco principal |
|---|-------|---------------|
| 0 | `staff-engineer-orchestrator` | Maestro — coordena, consolida, plano final |
| 1 | `dependency-versions-reviewer` | Versoes GA via WebSearch — Java, Python, Go, AWS runtimes |
| 2 | `tech-lead-reviewer` | Pragmatismo, simplicidade, manutenibilidade |
| 3 | `architect-reviewer` | Boundaries, resiliencia, contratos |
| 4 | `api-contract-reviewer` | OpenAPI, Protobuf, GraphQL, Avro, AsyncAPI |
| 5 | `security-reviewer` | Seguranca, hardening, superficies de abuso |
| 6 | `compliance-reviewer` | LGPD, GDPR, residencia de dados, serverless compliance |
| 7 | `ad-dba-reviewer` | Dados, modelagem, queries, persistencia |
| 8 | `data-engineering-aws-architect` | Pipelines, Glue, EMR, Kinesis, Athena — trade-offs de dados AWS |
| 9 | `java-specialist` | Java 25, Spring Boot, Quarkus, Micronaut |
| 10 | `python-specialist` | Python, pyproject.toml, pytest, Ruff, Lambda Python |
| 11 | `go-specialist` | Go, go.mod, interfaces, context, table-driven tests |
| 12 | `software-engineer` | Implementacao minima correta (poliglota) |
| 13 | `sre-platform-engineer` | Operabilidade, deploy, IaC, observabilidade |
| 14 | `finops-reviewer` | Custo AWS, rightsizing, anti-padroes de billing |
| 15 | `devex-reviewer` | Onboarding, ambiente local, Dev Container (poliglota) |
| 16 | `qa-quality-engineer` | Testes, qualidade, edge cases, regressoes |
| 17 | `performance-reliability-reviewer` | Throughput, latencia, escalabilidade |
| 18 | `tech-writer` | README, getting-started, testing, troubleshooting |

---

## Arquitetura de dois níveis

O kit usa dois níveis complementares:

| Nível | Caminho | Função |
|-------|---------|--------|
| Instruções da skill | `.agents/skills/<nome>/SKILL.md` | Papel, escopo, regras, checklist e formato de saída |
| Runtime do agente | `.codex/agents/<nome>.toml` | Modelo, sandbox, instruções de escopo para o Codex CLI |

O `.codex/config.toml` define parâmetros globais de execução:

```toml
[agents]
max_threads = 6   # paralelismo máximo
max_depth = 1     # hierarquia plana intencional
```

`max_depth = 1` é **intencional**: o orquestrador pode acionar especialistas, mas especialistas não acionam outros agentes. Isso evita recursão e mantém o fluxo previsível.

Prioridade de regras: `AGENTS.md` > `.codex/agents/*.toml` > `.agents/skills/*/SKILL.md`.

---

## Como funciona tecnicamente

O `staff-engineer-orchestrator` é o ponto de entrada para demandas não triviais. Sua saída segue sempre 23 seções fixas:

```
1.  Diagnóstico inicial                    → O que foi pedido e o contexto
2.  Stack e módulos impactados             → Tecnologias e áreas afetadas
3.  Versões de dependências validadas      → Via dependency-versions-reviewer (WebSearch)
4.  Achados do Tech Lead                   → Pragmatismo e manutenção
5.  Achados do Architect                   → Arquitetura e boundaries
6.  Achados do API Contract                → Contratos, breaking changes
7.  Achados do Security                    → Segurança e riscos
8.  Achados do Compliance                  → LGPD, GDPR, residência de dados
9.  Achados do AD/DBA                      → Dados e persistência
10. Achados do Data Engineering            → Pipelines, ETL, streaming (quando aplicável)
11. Achados do Language Specialist         → Java / Python / Go (conforme stack)
12. Achados do Software Engineer           → Implementação proposta
13. Achados do SRE/Platform                → Operabilidade e deploy
14. Achados do FinOps                      → Custo AWS e anti-padrões de billing
15. Achados do DevEx                       → Onboarding e ambiente local
16. Achados do QA/Quality                  → Testes e qualidade
17. Achados do Performance                 → Performance e confiabilidade
18. Achados do Tech Writer                 → Documentação impactada (quando aplicável)
19. Conflitos entre recomendações          → Divergências e resolução
20. Plano final priorizado                 → Ações ordenadas por prioridade
21. Diff sugerido                          → Mudanças concretas
22. Riscos remanescentes                   → O que ainda pode dar errado
23. Estratégia de validação                → Como confirmar que está correto
```

Essa estrutura fixa garante rastreabilidade e completude — voce sabe de onde veio cada recomendacao.

---

## Como utilizar multiagentes no dia a dia

### Fluxo recomendado (demanda nao trivial)

1. Passe o contexto completo da demanda.
2. Inicie pelo `staff-engineer-orchestrator`.
3. Exija consulta das skills relevantes antes de implementar.
4. Implemente somente apos plano consolidado.

Exemplo de prompt:

```text
Atue como staff-engineer-orchestrator seguindo AGENTS.md.
Leia .agents/skills/staff-engineer-orchestrator/SKILL.md para sua definicao completa.

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
Com base no plano consolidado, atue como software-engineer seguindo
.agents/skills/software-engineer/SKILL.md e implemente
apenas a menor mudanca correta, preservando backward compatibility.
Liste arquivos alterados, riscos remanescentes e comandos de validacao.
```

---

## Verificacao rapida (se esta "certinho")

**Bash:**

```bash
ls .agents/skills/
ls .codex/agents/
cat .codex/config.toml
```

**PowerShell:**

```powershell
Get-ChildItem .agents/skills -Directory | Select-Object -ExpandProperty Name
Get-ChildItem .codex/agents/*.toml | Select-Object -ExpandProperty Name
Get-Content .codex/config.toml
```

Se os nomes de skills em `.agents/skills` e `.codex/agents` estiverem alinhados, a base multiagente esta consistente.

---

## Como adicionar uma nova skill

1. Crie o arquivo em `.agents/skills/<nome>/SKILL.md`.
2. Crie o agente correspondente em `.codex/agents/<nome>.toml`.
3. Atualize a ordem de consulta no `AGENTS.md` e no `staff-engineer-orchestrator/SKILL.md` quando necessario.
4. Atualize a tabela de agentes neste `README.md`.
5. Atualize a tabela de comparacao no `README.md` da raiz do repositorio (se o papel for novo no projeto inteiro).

---

## Notas de compatibilidade

- O repositorio usa a estrutura atual (`.agents/skills` + `.codex/agents`).
- Se encontrar referencia textual a `codex/skills/`, trate como **legado** e use `.agents/skills/`.
- A stack Java/AWS no `AGENTS.md` e **contexto-alvo para projetos consumidores**, nao codigo executavel neste repositorio.
