# Software Engineering Process

Processo de engenharia de software para sistemas críticos.

## 1. Design → Implementação → Validação → Deploy

```
[Requisito] → [Design] → [Implementação] → [Code Review] → [CI/CD] → [Deploy] → [Operação]
                 ↓              ↓               ↓              ↓           ↓
              ADR/Doc      Testes junto    Feedback loop    Quality     Observar
                          com código      (< 24h)          gates       métricas
```

## 2. Design — Antes de escrever código

### Quando fazer design formal
| Cenário | Ação |
|---------|------|
| Bugfix pontual | Não precisa — corrija e teste |
| Feature pequena (1-3 arquivos) | Design mental, talvez um comentário |
| Feature média (novo endpoint, novo consumer) | Discuss com o time, document decisão |
| Feature grande (novo serviço, nova integração) | ADR + diagramas + revisão |
| Mudança arquitetural | ADR obrigatório + revisão com seniors |

### ADR (Architecture Decision Record) — Template
```markdown
# ADR-NNNN: [Título da decisão]

## Status: Proposed / Accepted / Deprecated / Superseded

## Context
O que motivou essa decisão? Qual problema estamos resolvendo?

## Decision
O que decidimos fazer?

## Consequences
### Positivas
### Negativas
### Riscos

## Alternatives considered
O que mais avaliamos e por que descartamos?
```

## 3. Implementação — Boas práticas

### Commits atômicos
- Um commit = uma mudança lógica
- Commit compila e testes passam
- Mensagem segue Conventional Commits

### Branch strategy
```
main ← PR ← feature/xxx
         ← bugfix/xxx
         ← hotfix/xxx
```

### Tamanho de PR
| Linhas alteradas | Classificação | Recomendação |
|-----------------|---------------|--------------|
| < 100 | Pequeno | Ideal |
| 100-400 | Médio | OK |
| 400-800 | Grande | Considere split |
| > 800 | Muito grande | Split obrigatório |

### Princípios de implementação
1. **YAGNI** — Não construa o que não precisa agora
2. **KISS** — A solução mais simples que funciona
3. **DRY** — Mas não prematuramente (3 repetições → abstrair)
4. **Fail fast** — Valide input nas bordas
5. **Defense in depth** — Não confie em uma única validação

## 4. Code Review — O que avaliar

### Correção funcional
- O código faz o que deveria?
- Edge cases tratados?
- Erros tratados corretamente?

### Design
- Responsabilidades claras?
- Acoplamento baixo?
- Interfaces no nível certo de abstração?

### Manutenibilidade
- Outro dev entenderia em 6 meses?
- Nomes claros?
- Sem complexidade acidental?

### Performance (quando relevante)
- Queries N+1?
- Loops desnecessários?
- Alocações excessivas?

### Segurança
- Input validado?
- Sem injection?
- Sem segredos?

### Tempo de review
- PR pequeno: review em < 4h
- PR médio: review em < 24h
- PR grande: considere pair programming

## 5. CI/CD — Pipeline mínima

```
[Push] → Lint → Unit Test → SAST → Build → Integration Test → Deploy Staging → Smoke Test → Deploy Prod
```

### Quality gates (bloqueiam deploy)
- Lint com zero erros
- Testes com zero falhas
- Cobertura acima do threshold
- SAST sem achados critical
- Vulnerabilidades de dependência resolvidas

## 6. Deploy — Estratégias

| Estratégia | Risco | Rollback | Quando usar |
|-----------|-------|----------|-------------|
| Blue/Green | Baixo | Instantâneo (switch) | Default para produção |
| Canary | Baixo | Rápido (shift traffic) | Features arriscadas |
| Rolling | Médio | Médio (wait + rollback) | Serviços stateless |
| Big bang | Alto | Lento | Nunca em produção |

### Rollback checklist
- [ ] Como detectar que precisa rollback? (alarmes)
- [ ] Como executar rollback? (runbook)
- [ ] Quanto tempo leva? (< 5 min)
- [ ] Migrations são backward-compatible?
- [ ] Quem decide? (oncall)

## 7. Operação — Dia 2

### Observabilidade mínima
- Logs estruturados JSON
- Métricas RED por endpoint
- Alertas para error rate e latência
- Tracing distribuído (quando multi-serviço)

### Incident response
1. **Detect**: alarme dispara
2. **Triage**: severidade + impacto
3. **Mitigate**: restaurar serviço (rollback, toggle, scale)
4. **Resolve**: corrigir causa raiz
5. **Postmortem**: documentar + ações

### SLOs mínimos
| Componente | SLI | SLO |
|-----------|-----|-----|
| API | Availability | 99.9% |
| API | Latency p99 | < 500ms |
| Consumer | Processing rate | 99.5% |
| Consumer | Lag | < 30s |

## Checklist de maturidade
- [ ] Processo de code review definido?
- [ ] CI/CD automatizado?
- [ ] Quality gates bloqueando deploy?
- [ ] Deploy em < 30 min do merge?
- [ ] Rollback em < 5 min?
- [ ] Observabilidade dos 3 pilares?
- [ ] Alertas para cenários críticos?
- [ ] Runbooks para alarmes?
- [ ] Postmortem após incidentes?
- [ ] ADRs para decisões significativas?
