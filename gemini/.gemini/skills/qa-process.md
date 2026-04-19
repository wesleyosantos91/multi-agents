# QA Process — Software Quality Engineering

Processo completo de qualidade para entregas de software.

## 1. Pirâmide de testes — Quanto testar?

```
                    /  E2E (5%)   \        Fluxos críticos do usuário
                   /--------------\
                  / Integration    \       Bordas, APIs, banco, mensageria
                 /  (20%)          \
                /-------------------\
               /    Unit (75%)       \     Lógica de negócio, regras, cálculos
              /_______________________\
```

### Regra prática
| Tipo de código | Tipo de teste | Prioridade |
|---------------|---------------|-----------|
| Regra de negócio | Unitário | Alta |
| Cálculos/transformações | Unitário + property-based | Alta |
| API endpoints | Integração (MockMvc/TestClient) | Alta |
| Persistência | Integração (Testcontainers) | Alta |
| Mensageria | Integração | Média |
| Clientes HTTP | Mock (WireMock/MSW) | Média |
| Fluxo completo do usuário | E2E (Playwright/Cypress) | Seletiva |

## 2. Critérios de aceite — Definition of Done

### Para qualquer feature
- [ ] Código implementado e compilando
- [ ] Testes unitários cobrindo happy path e edge cases
- [ ] Testes de integração para bordas impactadas
- [ ] Code review aprovado
- [ ] Sem regressões (testes existentes passando)
- [ ] Documentação atualizada (se comportamento mudou)

### Para features críticas (pagamentos, auth, dados sensíveis)
- [ ] Tudo acima +
- [ ] Revisão de segurança
- [ ] Testes de erro e falha (timeout, indisponibilidade)
- [ ] Idempotência validada (quando mensageria)
- [ ] Teste de carga básico (quando performance é requisito)

## 3. Análise de edge cases — Checklist mental

### Dados
- Null / None / nil
- String vazia vs null
- Lista vazia vs null
- Números: zero, negativo, máximo, overflow
- Datas: fuso horário, DST, leap year, epoch
- Unicode, caracteres especiais, emoji
- Payload muito grande (limite de tamanho)

### Estado
- Operação em estado inválido (cancelar pedido já cancelado)
- Operação concorrente (dois updates simultâneos)
- Operação parcial (falha no meio de batch)
- Retry (mesma operação 2x — idempotência)

### Dependências
- Timeout de dependência
- Dependência indisponível
- Resposta inesperada (500, body malformado)
- Latência alta (slow response)

### Bordas HTTP
- Request sem body
- Content-Type errado
- Header obrigatório faltando
- Path param inválido (letras onde espera número)
- Query param com valor malicioso (SQL injection)

## 4. Tipos de teste por cenário

### Happy path
O caminho normal de sucesso. SEMPRE testar primeiro.

### Sad path
Erros esperados e tratados:
- Validação de input falha → 400
- Recurso não encontrado → 404
- Regra de negócio violada → 422
- Rate limit → 429

### Evil path
Entradas maliciosas ou inesperadas:
- SQL injection em campos de texto
- Payload gigante (DDoS via payload)
- Headers manipulados
- Paths com traversal (`../../etc/passwd`)

### Failure path
Falhas de infraestrutura:
- Banco indisponível
- Fila cheia
- Timeout de serviço externo
- Disco cheio / memória esgotada

## 5. Regressão — Quando testar o quê

### Em todo PR
- Testes unitários (< 2 min)
- Lint / SAST
- Testes de integração do módulo alterado

### Antes de release
- Suite completa de integração
- E2E dos fluxos críticos
- Smoke test em staging

### Periodicamente (semanal)
- Scan de vulnerabilidades de dependência
- Testes de performance baseline
- Testes de contrato (consumer-driven)

## 6. Quality gates em CI

```yaml
# Pipeline mínima de qualidade
lint:        # Ruff/golangci-lint/checkstyle
unit-test:   # Testes unitários + cobertura
sast:        # Semgrep/CodeQL/bandit
integration: # Testes de integração
dep-scan:    # pip-audit/govulncheck/OWASP
```

### Métricas de qualidade
| Métrica | Threshold mínimo |
|---------|-----------------|
| Cobertura de linhas | 80% código novo |
| Cobertura de mutação (PIT) | 70% código crítico |
| Bugs SAST | 0 critical/high |
| Vulnerabilidades deps | 0 critical |
| Testes falhando | 0 |

## 7. Relatório de qualidade — Template

```markdown
## Quality Report — [Feature/PR]

### Cobertura
- Unitários: X testes, Y% cobertura
- Integração: X testes
- E2E: X fluxos cobertos

### Edge cases cobertos
- [x] Null input
- [x] Concurrent access
- [x] Timeout de dependência
- [ ] Payload > 1MB (não aplicável)

### Riscos identificados
| Risco | Severidade | Mitigação |
|-------|-----------|-----------|
| ... | Alta | ... |

### Veredicto
**GO** / **NO-GO** — justificativa
```

## 8. Checklist de release
- [ ] Todos os testes passando em CI?
- [ ] Cobertura acima do threshold?
- [ ] Sem vulnerabilidades critical em deps?
- [ ] SAST sem achados critical?
- [ ] Smoke test em staging OK?
- [ ] Rollback documentado e testado?
- [ ] Monitoramento e alertas configurados?
- [ ] Feature flag (se gradual rollout)?
