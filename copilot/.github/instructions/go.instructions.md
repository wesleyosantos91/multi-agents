---
applyTo: "**/*.go,**/go.mod,**/go.sum"
---
# Go Instructions

- Use `internal/` como padrao — `pkg/` apenas quando ha real intencao de reuso por outros modulos.
- Nao crie `util/`, `common/`, `helpers/` — nomear por responsabilidade de dominio.
- `context.Context` como primeiro parametro em toda funcao que faz I/O ou pode ser cancelada.
- Erros com contexto: `fmt.Errorf("descricao do contexto: %w", err)`.
- Sem `panic` como controle de fluxo — apenas para invariantes de programacao irrecupera.
- Toda goroutine deve ter forma clara de encerramento (context, WaitGroup ou errgroup).
- Interfaces definidas no pacote consumidor, nao no implementador.
- Handler Lambda fino: extrai evento → delega para `internal/service/` → retorna.
- Sempre considerar impacto em testes (table-driven, `t.Run`, `-race` em CI).

## Referencias

- `docs/ai/roles/go-specialist.md`
- `docs/ai/roles/software-engineer.md`
- `docs/ai/orchestration/staff-engineer-orchestrator.md`
