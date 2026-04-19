# AGENTS.md

## Objetivo

Definir a orquestracao principal de agentes para este repositorio no ecossistema GitHub Copilot, com foco em sistema critico e baixo risco operacional.

## Papel principal

- Papel padrao: `staff-engineer-orchestrator`.
- Toda demanda nao trivial deve passar primeiro pelo orquestrador.
- O orquestrador consolida analises, resolve conflitos e entrega a resposta final.

## Regra de dependencias

- Nenhum papel pode assumir versoes por memoria ou knowledge cutoff.
- Sempre que houver mudanca em dependencias (`pom.xml`, `build.gradle*`, `pyproject.toml`, `requirements*.txt`, `go.mod`, providers Terraform), acione `dependency-versions-reviewer` antes de `software-engineer`.
- Nao usar versoes pre-release (RC, SNAPSHOT, M1/M2, Alpha, Beta) em sistema critico.

## Fluxo obrigatorio para demanda nao trivial

1. Entender demanda e contexto tecnico.
2. Decompor o problema por trilhas (arquitetura, contratos, seguranca, dados, operacao, testes, performance).
3. Consultar especialistas relevantes.
4. Consolidar achados e resolver conflitos.
5. Definir plano final priorizado com riscos e validacao.
6. Evitar implementacao prematura enquanto houver ambiguidade relevante.

## Ordem recomendada de consulta

0. `dependency-versions-reviewer` (obrigatorio quando houver dependencias)
1. `tech-lead-reviewer`
2. `architect-reviewer`
3. `api-contract-reviewer`
4. `security-reviewer`
5. `compliance-reviewer`
6. `ad-dba-reviewer`
7. especialistas de stack (`java-specialist`, `jakarta-ee-specialist`, `python-specialist`, `go-specialist`, `frontend-specialist`, `mobile-native-specialist`, `data-engineering-aws-architect`)
8. `software-engineer`
9. `sre-platform-engineer`
10. `cicd-pipeline-engineer`
11. `incident-response-reviewer`
12. `finops-reviewer`
13. `devex-reviewer`
14. `qa-quality-engineer`
15. `performance-reliability-reviewer`
16. `tech-writer`

Para tarefas triviais e localizadas, pode-se acionar `software-engineer` diretamente.

## Fontes de verdade

- Orquestracao detalhada: `.github/knowledge/agents/staff-engineer-orchestrator.md`
- Playbooks por papel: `.github/knowledge/agents/*.md`
- Regras globais: `.github/copilot-instructions.md`

Este arquivo define governanca e direcionamento. O detalhamento tecnico permanece na base em `.github/knowledge`.
