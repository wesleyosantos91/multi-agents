---
applyTo: "**/src/main/**,**/src/test/**,**/application*.yml,**/application*.yaml,**/application*.properties"
---
# Framework Instructions

- Respeite o framework do modulo impactado; nao misture estilos de Spring Boot, Quarkus e Micronaut sem necessidade.
- Preservar configuracao explicita por ambiente, evitando comportamento ambiguo em runtime.
- Garantir testabilidade e operabilidade desde o design (health checks, logs, metricas, tracing).
- Mudancas de framework ou padrao estrutural exigem justificativa tecnica clara e analise do orquestrador.
- Em sistema critico, privilegie previsibilidade operacional sobre ganhos marginais de curto prazo.

## Referencias

- `docs/ai/roles/architect-reviewer.md`
- `docs/ai/roles/sre-platform-engineer.md`
- `docs/ai/roles/software-engineer.md`
