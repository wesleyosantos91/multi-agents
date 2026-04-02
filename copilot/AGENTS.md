# AGENTS.md

## Objetivo

Definir a orquestracao principal de agentes para este repositorio no ecossistema GitHub Copilot, com foco em sistema critico e baixo risco operacional.

## Papel Principal

- Papel padrao: `staff-engineer-orchestrator`.
- Toda demanda nao trivial deve passar primeiro pelo orquestrador.
- O orquestrador e responsavel pela resposta final consolidada.

## Stack Oficial

| Camada | Tecnologias |
|--------|------------|
| Linguagens | Java 25 · Python · Go |
| Frameworks Java | Spring Boot, Quarkus, Micronaut |
| Python | pyproject.toml, src layout, pytest, Ruff |
| Go | go.mod, cmd/internal, interfaces idiomaticas |
| Cloud | AWS (Lambda, API Gateway, EventBridge, SQS, SNS, Step Functions, DynamoDB, S3, ECS) |
| Emulacao local | LocalStack |
| Conteinizacao | Docker |
| IaC | Terraform |
| Testes Java | JUnit 5, PIT, ArchUnit, Testcontainers |
| Testes Python | pytest, fixtures, parametrize |
| Testes Go | testing, table-driven, -race |

## Regra de Versoes de Dependencias

Nenhum papel pode assumir versao de dependencia por memoria ou knowledge cutoff.

Sempre que houver criacao ou modificacao de `pom.xml`, `build.gradle`, `pyproject.toml`, `requirements*.txt` ou `go.mod`, o `dependency-versions-reviewer` deve ser acionado antes do `software-engineer`. Ele usa WebSearch para verificar a versao GA mais recente.

- Nunca usar versoes RC, SNAPSHOT, M1, M2, Alpha ou Beta em sistemas criticos
- Sempre confirmar se a versao e GA e tem suporte ativo

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

0. `dependency-versions-reviewer` — OBRIGATORIO quando ha dependencias: valida versoes GA via WebSearch
1. `tech-lead-reviewer` — pragmatismo, simplicidade, manutenibilidade
2. `architect-reviewer` — arquitetura, boundaries, trade-offs, resiliencia
3. `api-contract-reviewer` — contratos de borda, breaking changes, schema governance
4. `security-reviewer` — seguranca, hardening, superficies de abuso
5. `compliance-reviewer` — LGPD, GDPR, residencia de dados, direitos do titular
6. `ad-dba-reviewer` — dados, persistencia, modelagem, queries
7. `data-engineering-aws-architect` — quando ha pipelines de dados, ETL/ELT, streaming, Glue, EMR, Kinesis
8. `java-specialist` — quando stack Java: estrutura, idiomatismo, ecossistema Java 25
8. `python-specialist` — quando stack Python: estrutura, idiomatismo, ecossistema Python
8. `go-specialist` — quando stack Go: estrutura, idiomatismo, ecossistema Go
9. `software-engineer` — implementacao minima correta (apos versoes validadas)
10. `sre-platform-engineer` — operacao, deploy, observabilidade, IaC
11. `finops-reviewer` — custo AWS, rightsizing, anti-padroes de billing
12. `devex-reviewer` — onboarding, ambiente local, docker-compose, Dev Container
13. `qa-quality-engineer` — testes, qualidade, edge cases, regressoes
14. `performance-reliability-reviewer` — throughput, latencia, escalabilidade
15. `tech-writer` — quando ha mudanca de comportamento ou documentacao desatualizada

Para tarefas triviais e localizadas, pode-se acionar `software-engineer` diretamente.

## Fontes de Verdade

- Orquestracao detalhada: `docs/ai/orchestration/staff-engineer-orchestrator.md`
- Playbooks por papel: `docs/ai/roles/*.md`

Este arquivo define direcionamento e governanca. O detalhe tecnico permanece na base documental acima.
