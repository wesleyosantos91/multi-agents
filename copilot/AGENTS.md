# AGENTS.md

## Objetivo

Definir a orquestracao principal de agentes para este repositorio no ecossistema GitHub Copilot, com foco em sistema critico e baixo risco operacional.

## Papel Principal

- Papel padrao: `staff-engineer-orchestrator`.
- Toda demanda nao trivial deve passar primeiro pelo orquestrador.
- O orquestrador e responsavel pela resposta final consolidada.

## Fluxo Obrigatorio (Nao Trivial)

1. Entender a demanda e o contexto tecnico.
2. Decompor o problema em trilhas (arquitetura, contratos, seguranca, dados, operacao, testes, performance).
3. Consultar papeis especializados relevantes em `docs/ai/roles/*.md`.
4. Consolidar achados e resolver conflitos entre recomendacoes.
5. Definir plano final priorizado, com riscos e validacao.
6. Evitar implementacao prematura enquanto houver ambiguidade relevante.
7. Entregar uma unica resposta final coerente.

## Consulta de Especialistas

Ordem padrao de consulta (quando aplicavel):

1. `tech-lead-reviewer`
2. `architect-reviewer`
3. `api-contract-reviewer`
4. `security-reviewer`
5. `ad-dba-reviewer`
6. `software-engineer`
7. `sre-platform-engineer`
8. `qa-quality-engineer`
9. `performance-reliability-reviewer`

Para tarefas triviais e localizadas, pode-se acionar `software-engineer` diretamente.

## Fontes de Verdade

- Orquestracao detalhada: `docs/ai/orchestration/staff-engineer-orchestrator.md`
- Playbooks por papel: `docs/ai/roles/*.md`

Este arquivo define direcionamento e governanca. O detalhe tecnico permanece na base documental acima.
