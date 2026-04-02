# Multi-Agent Copilot Playbook

## Visao geral

Este repositorio implementa um modelo de multiagentes para GitHub Copilot com uma regra central:

- demandas nao triviais passam primeiro pelo `staff-engineer-orchestrator`
- especialistas sao consultados por tema
- a resposta final e consolidada em um unico plano priorizado

A estrategia foi desenhada para sistema critico, com foco em resiliencia, seguranca, observabilidade, operabilidade e menor risco de producao.

## Pre-requisitos

Para usar este modulo com GitHub Copilot em modo agente, voce precisa de:

- **VS Code 1.99 ou superior** — versao minima com suporte a agentes customizados no Copilot Chat
- **Extensao GitHub Copilot** atualizada (versao compativel com agent mode)
- **Plano GitHub Copilot Pro, Business ou Enterprise** — o modo agente nao esta disponivel no plano Free
- **Agent mode habilitado** no VS Code: no painel do Copilot Chat, selecione **Agent** no seletor de modo (em vez de Ask ou Edit)

> Para verificar sua versao do VS Code: `Ajuda > Sobre`. Para verificar o plano: acesse `github.com/settings/copilot`.

## Objetivo do staff-engineer-orchestrator

O `staff-engineer-orchestrator` e o maestro do processo. Ele:

1. entende a demanda e o contexto tecnico
2. decompoe o problema por frentes
3. consulta especialistas relevantes
4. consolida achados e resolve conflitos
5. entrega plano final priorizado com riscos e validacao

Para detalhes completos do comportamento esperado, consulte `docs/ai/orchestration/staff-engineer-orchestrator.md`.

## Papel dos agentes especializados

Os especialistas representam perspectivas tecnicas independentes:

- `dependency-versions-reviewer`: versoes GA via WebSearch — Java, Python, Go, AWS runtimes
- `tech-lead-reviewer`: simplicidade, pragmatismo, manutencao
- `architect-reviewer`: boundaries, trade-offs, resiliencia estrutural
- `api-contract-reviewer`: contratos e compatibilidade evolutiva
- `security-reviewer`: auth/authz, segredos, hardening, abuso
- `compliance-reviewer`: LGPD, GDPR, residencia de dados, direitos do titular
- `ad-dba-reviewer`: dados, modelagem, consultas, indices
- `data-engineering-aws-architect`: pipelines, ETL/ELT, Glue, EMR, Kinesis, trade-offs de dados AWS
- `java-specialist`: Java 25, Spring Boot, Quarkus, Micronaut
- `python-specialist`: Python, pyproject.toml, pytest, Ruff, Lambda Python
- `go-specialist`: Go, go.mod, interfaces, context, table-driven tests
- `software-engineer`: implementacao minima correta (poliglota)
- `sre-platform-engineer`: operacao, deploy, observabilidade, IaC
- `finops-reviewer`: custo AWS, rightsizing, anti-padroes de billing
- `devex-reviewer`: onboarding, ambiente local, Dev Container (poliglota)
- `qa-quality-engineer`: testes, regressao, edge cases, risco de producao
- `performance-reliability-reviewer`: latencia, throughput, confiabilidade e escala
- `tech-writer`: README, getting-started, testing, troubleshooting

## Camadas de customizacao

| Camada | Funcao | Nivel de detalhe |
|---|---|---|
| `AGENTS.md` | regra principal de orquestracao e roteamento | enxuto |
| `.github/copilot-instructions.md` | guardrails globais do repositorio | enxuto |
| `.github/instructions/*.instructions.md` | regras contextuais por path/tema (`applyTo`) | medio |
| `.github/agents/*.agent.md` | perfis dos agentes customizados | medio |
| `docs/ai/orchestration/*.md` | playbook detalhado do orquestrador | alto |
| `docs/ai/roles/*.md` | playbooks detalhados por papel | alto |

## Estrutura do repositorio

```text
copilot/
├── AGENTS.md
├── .github/
│   ├── copilot-instructions.md
│   ├── instructions/
│   │   ├── api.instructions.md
│   │   ├── frameworks.instructions.md
│   │   ├── go.instructions.md
│   │   ├── java.instructions.md
│   │   ├── messaging.instructions.md
│   │   ├── python.instructions.md
│   │   ├── security.instructions.md
│   │   ├── terraform.instructions.md
│   │   └── testing.instructions.md
│   └── agents/
│       ├── ad-dba-reviewer.agent.md
│       ├── api-contract-reviewer.agent.md
│       ├── architect-reviewer.agent.md
│       ├── compliance-reviewer.agent.md
│       ├── data-engineering-aws-architect.agent.md
│       ├── dependency-versions-reviewer.agent.md
│       ├── devex-reviewer.agent.md
│       ├── finops-reviewer.agent.md
│       ├── go-specialist.agent.md
│       ├── java-specialist.agent.md
│       ├── performance-reliability-reviewer.agent.md
│       ├── python-specialist.agent.md
│       ├── qa-quality-engineer.agent.md
│       ├── security-reviewer.agent.md
│       ├── software-engineer.agent.md
│       ├── sre-platform-engineer.agent.md
│       ├── staff-engineer-orchestrator.agent.md
│       ├── tech-lead-reviewer.agent.md
│       └── tech-writer.agent.md
└── docs/ai/
    ├── orchestration/
    │   └── staff-engineer-orchestrator.md
    └── roles/
        ├── ad-dba-reviewer.md
        ├── api-contract-reviewer.md
        ├── architect-reviewer.md
        ├── compliance-reviewer.md
        ├── data-engineering-aws-architect.md
        ├── dependency-versions-reviewer.md
        ├── devex-reviewer.md
        ├── finops-reviewer.md
        ├── go-specialist.md
        ├── java-specialist.md
        ├── performance-reliability-reviewer.md
        ├── python-specialist.md
        ├── qa-quality-engineer.md
        ├── security-reviewer.md
        ├── software-engineer.md
        ├── sre-platform-engineer.md
        ├── tech-lead-reviewer.md
        └── tech-writer.md
```

## Como adotar em seu repositorio

Para usar esta estrutura em um repositorio existente:

1. Copie as pastas `.github/agents/`, `.github/instructions/` e o arquivo `.github/copilot-instructions.md` para a raiz do seu repositorio.
2. Copie a pasta `docs/ai/` para a raiz do seu repositorio.
3. Copie o arquivo `AGENTS.md` para a raiz do seu repositorio.
4. Abra o VS Code com a extensao GitHub Copilot instalada e ativa.
5. Abra o Copilot Chat (`Ctrl+Alt+I`), ative o **agent mode** no seletor de modo e selecione o agente desejado.
6. Adapte o conteudo de `.github/copilot-instructions.md` e `docs/ai/orchestration/staff-engineer-orchestrator.md` para refletir o stack e os modulos do seu repositorio.

> Os agentes referenciam paths como `docs/ai/roles/*.md` — mantenha essa estrutura de pastas para que as referencias funcionem corretamente.

## Quando usar o orquestrador

Use `staff-engineer-orchestrator` quando houver pelo menos um destes sinais:

- impacto em mais de um modulo/camada
- mudanca de contrato (API/evento/schema)
- risco de seguranca, dados, operacao ou performance
- refatoracao com trade-offs arquiteturais
- mudanca com alto impacto de producao

## Quando usar um especialista diretamente

Use agente especializado direto quando a demanda for localizada e de baixa ambiguidade.

Exemplos:

- `security-reviewer`: revisao pontual de hardening
- `ad-dba-reviewer`: revisao de indice/query especifica
- `software-engineer`: ajuste pequeno e objetivo

Se durante a execucao surgir risco transversal, retorne ao `staff-engineer-orchestrator`.

## Exemplos praticos de prompts

### 1) Analise arquitetural

```text
Atue como staff-engineer-orchestrator.
Analise a proposta de criar uma nova borda gRPC para o modulo de faturamento.
Consulte os papeis necessarios, consolide conflitos e entregue plano final priorizado.
Contexto adicional: [descreva aqui].
```

### 2) Revisao de seguranca

```text
Atue como security-reviewer.
Revise autenticacao, autorizacao e exposicao de dados do endpoint /api/v1/payments.
Liste riscos criticos/medios e correcoes recomendadas.
```

### 3) Revisao de persistencia

```text
Atue como ad-dba-reviewer.
Avalie modelagem, indices e queries do fluxo de pedidos, incluindo paginacao e concorrencia.
Sugira a menor mudanca segura para reduzir custo e latencia.
```

### 4) Plano de upgrade/migracao

```text
Atue como staff-engineer-orchestrator.
Monte plano de migracao do contrato de eventos de OrderCreated v1 para v2 sem quebra.
Considere compatibilidade, rollout gradual, rollback e validacao.
```

### 5) Implementacao simples

```text
Atue como software-engineer.
Implemente a menor mudanca correta para corrigir validacao de status no endpoint de pedidos.
Nao refatore fora do escopo; inclua como validar.
```

## Fluxo recomendado para demandas nao triviais

1. Definir problema, impacto e risco de negocio/tecnico.
2. Acionar `staff-engineer-orchestrator`.
3. Consultar especialistas relevantes conforme contexto.
4. Consolidar conflitos e decidir trade-offs explicitamente.
5. Executar implementacao minima segura.
6. Validar com testes e criterios operacionais antes de rollout.

## Boas praticas de uso

- Contextualize stack, modulo e objetivo no prompt.
- Diga explicitamente o nivel de risco (critico, moderado, baixo).
- Solicite priorizacao por impacto e esforco.
- Mantenha mudancas pequenas e verificaveis.
- Referencie arquivos reais do repositorio sempre que possivel.
- Use `docs/ai/...` para detalhes; evite replicar playbook em prompts longos.

## Limitacoes do mecanismo

- Nao ha garantias formais de execucao serial de especialistas; a orquestracao depende do prompt e da disciplina de uso.
- Conflitos de recomendacao exigem consolidacao explicita pelo orquestrador.
- Em tarefas muito grandes, ainda e necessario quebrar o trabalho em incrementos.
- A qualidade da resposta depende da qualidade do contexto informado.

## Como evoluir sem duplicacao

1. Ajuste regras detalhadas apenas em `docs/ai/orchestration/` e `docs/ai/roles/`.
2. Mantenha `AGENTS.md` e `.github/copilot-instructions.md` enxutos (governanca e roteamento).
3. Use `.github/instructions/*.instructions.md` apenas para guardrails contextuais reutilizaveis.
4. Nos agentes em `.github/agents/`, descreva objetivo e limites; referencie playbooks ao inves de copiar.
5. Revise periodicamente consistencia entre camadas ao adicionar novo papel ou nova tecnologia.

## Como invocar agentes no Copilot Chat

### Abrindo o Copilot Chat

Abra o painel com `Ctrl+Alt+I` (Windows/Linux) ou `Cmd+Option+I` (macOS).

### Selecionando o modo agente

No campo de entrada do Copilot Chat, selecione **Agent** no seletor de modo. Somente neste modo os arquivos `.github/agents/*.agent.md` sao reconhecidos e os agentes aparecem no seletor.

### Selecionando um agente

Clique no seletor de agente (icone de robo ou dropdown de agentes) no campo de entrada. Os agentes customizados definidos em `.github/agents/` aparecem na lista com seus nomes e descricoes. Selecione o agente antes de enviar a mensagem.

Exemplos de uso:

```text
[staff-engineer-orchestrator selecionado no seletor]
Analise a proposta de criar uma nova borda gRPC para o modulo de faturamento.
Consulte os papeis necessarios, consolide conflitos e entregue plano final priorizado.
```

```text
[security-reviewer selecionado no seletor]
Revise autenticacao e autorizacao do endpoint /api/v1/payments.
Liste riscos criticos e medios com correcoes recomendadas.
```

### Diferenca do Claude Code

No GitHub Copilot, a selecao do agente e feita pela interface grafica — **nao use `@nome-do-agente`** no texto da mensagem. Alem disso, a consulta a especialistas pelo orquestrador nao e automatica: o orquestrador consulta especialistas por instrucao de prompt, nao por chamada nativa de sub-agente. Por isso, o prompt deve ser explicito sobre quais especialistas devem ser consultados quando necessario.

## Como criar um novo agente

### Passo 1: Crie o arquivo

Crie um arquivo em `.github/agents/` com o nome do agente e a extensao `.agent.md`:

```
.github/agents/meu-novo-agente.agent.md
```

### Passo 2: Defina o frontmatter YAML

```yaml
---
name: meu-novo-agente
description: Descricao objetiva do papel e quando usar este agente.
tools:
  - codebase
  - search
  - usages
---
```

| Campo | Descricao |
|---|---|
| `name` | Identificador unico. Deve ser unico entre os arquivos `.agent.md`. |
| `description` | Descricao curta. Aparece no seletor de agentes do Copilot Chat. |
| `tools` | Ferramentas disponiveis: `codebase`, `editFiles`, `runCommands`, `search`, `usages`, `problems`, `runTests`. Agentes de revisao usam apenas `codebase`, `search` e `usages`. |

### Passo 3: Escreva o corpo do agente

```markdown
# Nome do Agente

## Missao

Descricao clara do que este agente faz e seus limites.

## Quando Usar

- Cenario 1
- Cenario 2

## Regras de Atuacao

1. Regra obrigatoria 1
2. Regra obrigatoria 2

## Entrega Esperada

- Item de saida 1
- Item de saida 2

## Referencias

- `docs/ai/roles/meu-novo-agente.md`
- `docs/ai/orchestration/staff-engineer-orchestrator.md`
```

### Passo 4: Crie o playbook detalhado

Para manter o agente enxuto, crie o detalhamento em `docs/ai/roles/meu-novo-agente.md` e referencie a partir do arquivo `.agent.md`. Nao copie o conteudo do playbook para dentro do agente.

### Passo 5: Registre no orquestrador (se aplicavel)

Se o novo agente deve ser consultado pelo `staff-engineer-orchestrator`:

1. Adicione-o na lista de `## Consulta de Especialistas` em `AGENTS.md`.
2. Referencie-o no playbook `docs/ai/orchestration/staff-engineer-orchestrator.md`.

## Como adicionar um novo arquivo de instrucoes

Arquivos em `.github/instructions/` definem regras contextuais que o Copilot aplica automaticamente quando os arquivos abertos no editor correspondem ao padrao `applyTo`.

### Passo 1: Crie o arquivo

```
.github/instructions/meu-tema.instructions.md
```

### Passo 2: Defina o frontmatter com o padrao `applyTo`

```yaml
---
applyTo: "**/*.java,**/pom.xml"
---
```

O campo `applyTo` aceita um glob (ou lista separada por virgula). O Copilot injeta as instrucoes automaticamente quando o arquivo ativo no editor corresponde ao padrao.

Exemplos de padroes usados neste repositorio:

| Arquivo | `applyTo` |
|---|---|
| `java.instructions.md` | `**/*.java,**/pom.xml,...` |
| `security.instructions.md` | `**/src/main/**,**/*.tf,...` |
| `testing.instructions.md` | `**/src/test/**,**/*Test.java,...` |
| `messaging.instructions.md` | `**/message/**,**/*kafka*/**,...` |

### Passo 3: Escreva as instrucoes

```markdown
# Titulo do Tema

- Regra 1
- Regra 2

## Referencias

- `docs/ai/roles/papel-relevante.md`
```

### Boas praticas

- Mantenha cada arquivo focado em um unico tema ou tecnologia.
- Nao replique conteudo ja presente em outros arquivos de instrucoes.
- Use `applyTo` especifico — globs muito amplos (ex.: `**/*`) diluem o foco das instrucoes.
- Referencie `docs/ai/roles/*.md` em vez de duplicar regras detalhadas.
