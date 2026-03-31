---
applyTo: "**/src/test/**,**/*Test.java,**/*IT.java,**/*IntegrationTest.java,**/pom.xml"
---
# Testing Instructions

- Testes devem ser deterministicos, reprodutiveis e focados em comportamento.
- Base obrigatoria: JUnit 5; usar PIT para logica critica e ArchUnit para boundaries.
- Use Testcontainers para integracao com dependencias reais, evitando mock excessivo de infraestrutura.
- Cubra contratos de borda (`web/` e `message/`) e cenarios de falha parcial.
- Inclua casos de regressao para mudancas de contrato, seguranca, dados e operacao.

## Referencias

- `docs/ai/roles/qa-quality-engineer.md`
- `docs/ai/roles/api-contract-reviewer.md`
- `docs/ai/roles/performance-reliability-reviewer.md`
