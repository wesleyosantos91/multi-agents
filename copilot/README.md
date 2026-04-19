# Multi-Agent Copilot Playbook

Guia operacional do setup de multiagentes com GitHub Copilot para este repositorio.

## Visao geral

Este projeto usa uma estrategia de orquestracao por papeis:

- `staff-engineer-orchestrator` como maestro para demandas nao triviais.
- 24 agentes especialistas para analises por dominio (arquitetura, contratos, seguranca, dados, operacao, qualidade).
- consolidacao final em uma unica resposta coerente, com plano priorizado e riscos.

## Camadas da configuracao

| Camada | Localizacao | Proposito |
|--------|-------------|-----------|
| Governanca principal | `AGENTS.md` | Fluxo obrigatorio, ordem de consulta dos 24 papeis |
| Regras globais | `.github/copilot-instructions.md` | Politicas transversais do repositorio |
| Regras contextuais | `.github/instructions/*.instructions.md` (19) | Regras por path/tecnologia via `applyTo` |
| Perfis de agente | `.github/agents/*.agent.md` (24) | Agentes customizados do Copilot |
| Playbooks detalhados | `.github/knowledge/agents/*.md` | Versao canonica e completa de cada papel |
| Prompts reutilizaveis | `.github/prompts/*.prompt.md` (34) | Fluxos recorrentes (review, adr, debug, etc.) |
| Skills | `.github/skills/<nome>/SKILL.md` (45) | Conhecimento procedural reutilizavel |
| Hooks e politicas | `.github/hooks/*.json` + scripts em `.github/hooks/scripts/` | Quality gates (PowerShell) |
| Settings | `.github/copilot/settings.json` (+ `settings.local.json` local) | Comportamento do Copilot no repo |
| Referencias de projeto | `.github/knowledge/docs-reference/` | Architecture, runbooks, SLOs, postmortems |

## Quando usar o orquestrador

Use `staff-engineer-orchestrator` quando houver:

- mudanca arquitetural
- impacto em contratos/API
- risco de seguranca ou compliance
- alteracao de persistencia ou operacao
- demanda multi-modulo/multi-stack

## Quando usar especialista direto

Use agente especializado diretamente para tarefas pontuais e delimitadas, por exemplo:

- `software-engineer` — implementacao localizada de baixo risco
- `qa-quality-engineer` — reforco de estrategia de testes
- `security-reviewer` — hardening/revisao de risco
- `ad-dba-reviewer` — modelagem e query tuning

## Fluxo recomendado (demanda nao trivial)

1. Acionar `staff-engineer-orchestrator`.
2. Fazer triagem de impacto e trilhas tecnicas.
3. Consultar especialistas relevantes (incluindo `dependency-versions-reviewer` quando houver dependencias).
4. Consolidar conflitos e trade-offs.
5. Definir plano final priorizado.
6. Implementar somente apos convergencia tecnica.
7. Validar com testes e checks operacionais.

## Exemplos praticos de prompts

- Analise arquitetural
  `Use o staff-engineer-orchestrator para avaliar a arquitetura do fluxo de pedidos e propor plano de evolucao com riscos e mitigacoes.`

- Revisao de seguranca
  `Use o security-reviewer para revisar autenticacao/autorizacao deste modulo e listar vulnerabilidades com severidade.`

- Plano de upgrade
  `Use o staff-engineer-orchestrator e o dependency-versions-reviewer para propor upgrade GA de dependencias com estrategia de validacao.`

---

## Como adicionar novas configuracoes

Todos os pontos de extensao do setup Copilot neste projeto.

### 1. Novo agente

**Arquivos**: `.github/agents/<nome>.agent.md` (perfil curto) + `.github/knowledge/agents/<nome>.md` (playbook detalhado)

Perfil em `.github/agents/<nome>.agent.md`:

```markdown
---
name: meu-novo-agente
description: Papel e foco em uma frase.
tools:
  - read
  - search
---
# Meu Novo Agente

Voce e o [papel] de um sistema critico. Foco em [objetivo].

## Escopo de revisao
- Item 1
- Item 2

## Regras mandatorias
- Regra 1

## Checklist de revisao
- [ ] Check 1?

## Modo rapido
- **Veredicto**: uma linha
- 3 bullets + acao prioritaria

## Formato de saida obrigatorio
### 1. Secao 1
### 2. Secao 2
```

Playbook em `.github/knowledge/agents/<nome>.md`: versao detalhada com tabelas, trade-offs, exemplos de codigo. O perfil aponta para ele como referencia canonica.

**Registrar o agente**:
1. Adicionar na ordem de consulta no `AGENTS.md` e no `.github/knowledge/agents/staff-engineer-orchestrator.md`.
2. Atualizar a secao de orquestracao se o papel altera o fluxo.

---

### 2. Nova instrucao contextual

**Arquivo**: `.github/instructions/<nome>.instructions.md`

```markdown
---
applyTo: "**/web/**,**/*.proto,**/*openapi*/**"
---
# API Instructions

- Contratos formais e evolutiveis (OpenAPI, Protobuf, GraphQL).
- Breaking changes devem ser explicitos e planejados.

## Referencia
- `.github/knowledge/agents/api-contract-reviewer.md`
```

O campo `applyTo` usa glob e ativa a instrucao apenas nos paths correspondentes — ideal para regras especificas de stack (Java, Python, Go, Terraform, security, testing, messaging, etc.).

---

### 3. Novo prompt reutilizavel

**Arquivo**: `.github/prompts/<nome>.prompt.md`

```markdown
---
description: "Prompt reutilizavel do fluxo <nome> para Copilot Chat."
---

Acione o `nome-do-agente` para [objetivo].

## Escopo
- Se nao houver argumento, [comportamento padrao]
- Se houver, [comportamento especifico]

## Entrada do usuario
{{ARGUMENTS}}
```

Prompts aparecem na paleta do Copilot Chat. `{{ARGUMENTS}}` e substituido pelo texto fornecido pelo usuario.

---

### 4. Nova skill

**Arquivo**: `.github/skills/<nome>/SKILL.md`

```markdown
---
name: minha-skill
description: Conhecimento procedural sobre X. Dispara quando o contexto envolve Y.
---

# Skill: minha-skill

## Quando aplicar
- Contexto A
- Contexto B

## Conteudo
Passos, exemplos e templates reutilizaveis.
```

Skills sao conhecimento procedural reutilizavel — carregadas quando o contexto da tarefa corresponde ao `description`.

---

### 5. Novo hook / quality gate

Edite `.github/hooks/quality-gates.json`:

```jsonc
{
  "version": 1,
  "hooks": {
    "sessionStart": [
      {
        "type": "command",
        "powershell": "Write-Host \"[quality-gates] Sessao iniciada.\""
      }
    ],
    "preToolUse": [
      {
        "type": "command",
        "powershell": "powershell -NoProfile -ExecutionPolicy Bypass -File .github/hooks/scripts/pre-tool-policy.ps1"
      }
    ],
    "postToolUse": [
      {
        "type": "command",
        "powershell": "powershell -NoProfile -ExecutionPolicy Bypass -File .github/hooks/scripts/post-tool-audit.ps1"
      }
    ]
  }
}
```

Scripts auxiliares ficam em `.github/hooks/scripts/*.ps1`. Para adicionar uma nova politica:
1. Crie o script PowerShell em `.github/hooks/scripts/<nome>.ps1`.
2. Registre a chamada no evento correspondente em `quality-gates.json`.

---

### 6. Nova configuracao do Copilot

Edite `.github/copilot/settings.json` (committado) e, se for override pessoal, use `.github/copilot/settings.local.json` (nao commitado):

```jsonc
{
  "enableCustomAgents": true,
  "enableCustomPrompts": true,
  "enableInstructions": true
}
```

---

### 7. Nova referencia de projeto

`.github/knowledge/docs-reference/` concentra documentacao operacional usada pelos agentes:
- `architecture/` — ADRs, diagramas C4
- `runbooks/` — procedimentos operacionais
- `slos/` — definicoes de SLO/SLI
- `postmortems/` — historico de incidentes
- `on-call/` — rotina de plantao

Adicione novos arquivos nesses diretorios e referencie-os nos playbooks em `.github/knowledge/agents/`.

---

### Checklist antes de mergear

- [ ] Perfil curto em `.github/agents/` e playbook detalhado em `.github/knowledge/agents/` (ambos sincronizados)?
- [ ] `AGENTS.md` atualizado com o novo papel/regra?
- [ ] Nova instrucao usa `applyTo` com glob correto (evitar escopo global desnecessario)?
- [ ] Prompt/skill tem `description` especifico para ativacao correta?
- [ ] Hook novo testado no Windows (PowerShell)?
- [ ] README atualizado com contagens e proposito do novo item?
- [ ] Paridade com as outras plataformas (`claude-code/`, `codex/`, `gemini/`)?

---

## Boas praticas

- manter `.github/copilot-instructions.md` enxuto e transversal
- colocar detalhe tecnico por papel em `.github/knowledge/agents/*`
- evitar duplicacao entre camadas (perfil curto + playbook detalhado e suficiente)
- preferir prompts reutilizaveis para tarefas recorrentes
- registrar decisoes arquiteturais em `.github/knowledge/docs-reference/architecture/`

## Limitacoes

- customizacoes de agentes e prompts evoluem com features do Copilot e podem mudar de comportamento
- instrucoes conflitantes entre camadas podem gerar comportamento nao deterministico
- em code review no GitHub.com ha limites de leitura de instrucoes longas — prefira perfis curtos + referencia aos playbooks

## Evolucao da estrutura sem duplicacao

1. Atualize primeiro os playbooks em `.github/knowledge/agents/*`.
2. Reflita apenas o necessario em `.github/agents/*.agent.md`.
3. Mantenha `AGENTS.md` como camada de governanca, nao como manual gigante.
4. Crie novas regras contextuais em `.github/instructions/*.instructions.md` com `applyTo` especifico.
5. Revise periodicamente links e referencias para evitar drift.

## Observacao

- `.github/copilot/settings.local.json` e arquivo local e nao deve ser commitado.
