---
applyTo: "**/*.java,**/pom.xml,**/build.gradle,**/build.gradle.kts,**/mvnw,**/mvnw.cmd"
---
# Java Instructions

- Use Java 25 como baseline para qualquer implementacao ou refatoracao.
- Priorize clareza, legibilidade e menor mudanca correta; evite abstracoes prematuras.
- Preserve boundaries do projeto (`domain/`, `core/`, `infrastructure/`, `web/`, `message/`).
- Em integracoes externas, explicite timeout/retry/circuit breaker quando aplicavel.
- Mantenha o estilo idiomatico do framework ativo no modulo (Spring, Quarkus ou Micronaut).
- Sempre considerar impacto em testes (JUnit 5), arquitetura (ArchUnit) e regressao.

## Referencias

- `docs/ai/roles/tech-lead-reviewer.md`
- `docs/ai/roles/software-engineer.md`
- `docs/ai/orchestration/staff-engineer-orchestrator.md`
