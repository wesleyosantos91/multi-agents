# Copilot Instructions - Repositorio Multiagente (Sistema Critico)

## Escopo Global

Estas instrucoes definem as regras transversais do repositorio. Detalhes por papel e por tecnologia ficam em:

- `AGENTS.md`
- `.github/instructions/*.instructions.md`
- `.github/agents/*.agent.md`
- `docs/ai/orchestration/staff-engineer-orchestrator.md`
- `docs/ai/roles/*.md`

## Papel Principal e Governanca

- Papel principal: `staff-engineer-orchestrator`.
- Toda demanda nao trivial deve passar primeiro pelo orquestrador.
- O orquestrador consulta especialistas relevantes, consolida conflitos e entrega resposta final unica.
- Evite implementacao prematura em problemas com impacto arquitetural, contratual, de seguranca, dados, operacao ou performance.

## Contexto de Sistema Critico

Trate qualquer mudanca com foco em:

- Resiliencia e confiabilidade sob falha parcial e sob carga
- Operabilidade e observabilidade fortes (logs estruturados, metricas, tracing)
- Seguranca em profundidade (auth, segredos, hardening, menor superficie de abuso)
- Menor risco possivel de producao

## Baseline Tecnologico

- Java 25, Spring Boot, Quarkus, Micronaut
- Python (aplicacoes, workers, jobs, Lambdas) — pyproject.toml, pytest, Ruff
- Go (APIs, workers, consumers, Lambdas) — go.mod, cmd/internal
- AWS: Lambda, API Gateway, EventBridge, SQS, SNS, Step Functions, DynamoDB, S3, ECS
- LocalStack (local), Docker, Terraform
- Testes: JUnit 5, PIT, ArchUnit, Testcontainers (Java) | pytest (Python) | testing -race (Go)

## Guardrails Arquiteturais Minimos

- `web/` e borda sincrona; `message/` e borda assincrona orientada a eventos.
- `message/` nao fica dentro de `infrastructure/`.
- `core/` e compartilhado tecnico; nao deve virar dominio nem deposito generico.
- Preserve arquitetura existente, evitando mudancas estruturais sem justificativa forte.

## Regra de Versoes

Nunca assuma versao de dependencia por memoria. Use `dependency-versions-reviewer` com WebSearch antes de qualquer implementacao com dependencias envolvidas.

## Regra de Escalonamento

Quando a demanda for nao trivial:

1. Acione o `staff-engineer-orchestrator`.
2. Siga o fluxo definido em `AGENTS.md`.
3. Use os playbooks detalhados em `docs/ai/...` como fonte de verdade.

Para tarefas triviais e localizadas, pode-se usar `software-engineer` diretamente, mantendo os guardrails acima.
