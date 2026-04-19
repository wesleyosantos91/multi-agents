---
applyTo: "**/pom.xml,**/build.gradle,**/build.gradle.kts,**/go.mod,**/go.sum,**/pyproject.toml,**/requirements*.txt,**/package.json"
---
# Dependencies Instructions

- Nunca assumir versao por memoria; validar versao GA antes de adotar.
- Evitar versoes pre-release em sistema critico (alpha, beta, rc, snapshot).
- Atualizacoes devem considerar compatibilidade, seguranca e impacto operacional.
- Mudancas de dependencia devem incluir estrategia de validacao de regressao.

## Referencia
- `.github/knowledge/agents/dependency-versions-reviewer.md`
