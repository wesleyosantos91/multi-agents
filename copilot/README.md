# Multi-Agent Copilot Playbook

Guia operacional do setup de multiagentes com GitHub Copilot para este repositorio.

## Visao geral

Este projeto usa uma estrategia de orquestracao por papeis:

- `staff-engineer-orchestrator` como maestro para demandas nao triviais.
- agentes especialistas para analises por dominio (arquitetura, contratos, seguranca, dados, operacao, qualidade).
- consolidacao final em uma unica resposta coerente, com plano priorizado e riscos.

## Camadas da configuracao

- `AGENTS.md`
  Instrucao principal de orquestracao. Define o papel maestro, fluxo obrigatorio e ordem de consulta.

- `.github/copilot-instructions.md`
  Regras globais transversais do repositorio.

- `.github/instructions/*.instructions.md`
  Regras por contexto/path com `applyTo`.

- `.github/agents/*.agent.md`
  Perfis de agentes customizados usados pelo Copilot.

- `.github/knowledge/agents/*.md`
  Base canonicamente detalhada de orquestracao e playbooks por papel.

- `.github/prompts/*.prompt.md`
  Prompts reutilizaveis para fluxos recorrentes de engenharia.

- `.github/skills/*/SKILL.md`
  Skills de conhecimento e processo para uso complementar.

- `.github/hooks/*`
  Quality gates e politicas de uso de ferramentas.

- `.github/copilot/settings*.json`
  Configuracao de comportamento para o repo (com override local em `settings.local.json`).

## Quando usar o orquestrador

Use `staff-engineer-orchestrator` quando houver:

- mudanca arquitetural
- impacto em contratos/API
- risco de seguranca ou compliance
- alteracao de persistencia ou operacao
- demanda multi-modulo/multi-stack

## Quando usar especialista direto

Use agente especializado diretamente para tarefas pontuais e delimitadas, por exemplo:

- `software-engineer`: implementacao localizada de baixo risco
- `qa-quality-engineer`: reforco de estrategia de testes
- `security-reviewer`: hardening/revisao de risco
- `ad-dba-reviewer`: modelagem e query tuning

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

- Revisao de persistencia
  `Use o ad-dba-reviewer para revisar modelagem e consultas desta feature, com recomendacoes de indices e impacto.`

- Plano de upgrade/migracao
  `Use o staff-engineer-orchestrator e o dependency-versions-reviewer para propor upgrade GA de dependencias com estrategia de validacao.`

- Implementacao simples
  `Use o software-engineer para corrigir este bug localizado sem refatoracao lateral e com teste de regressao.`

## Boas praticas

- manter `.github/copilot-instructions.md` enxuto e transversal
- colocar detalhe tecnico por papel em `.github/knowledge/agents/*`
- evitar duplicacao entre camadas
- preferir prompts reutilizaveis para tarefas recorrentes
- registrar decisoes arquiteturais em `.github/knowledge/docs-reference/architecture/`

## Limitacoes

- customizacoes de agentes e prompts evoluem por feature e ambiente do Copilot
- instrucoes conflitantes entre camadas podem gerar comportamento nao deterministico
- em code review no GitHub.com, ha limites de leitura de instrucoes longas

## Evolucao da estrutura sem duplicacao

1. Atualize primeiro os playbooks em `.github/knowledge/agents/*`.
2. Reflita apenas o necessario em `.github/agents/*.agent.md`.
3. Mantenha `AGENTS.md` como camada de governanca, nao como manual gigante.
4. Crie novas regras contextuais em `.github/instructions/*.instructions.md` com `applyTo` especifico.
5. Revise periodicamente links e referencias para evitar drift.

## Observacao

- `.github/copilot/settings.local.json` e arquivo local e nao deve ser commitado.
