Identifique e priorize débito técnico no módulo ou projeto especificado.

## Processo

### 1. Varredura
- Busque TODOs, FIXMEs, HACKs, XXX no código (Grep)
- Identifique código duplicado evidente
- Identifique dependências desatualizadas ou deprecated
- Identifique testes faltantes em código crítico
- Identifique configurações hardcoded que deveriam ser externalizadas

### 2. Classificação
Para cada item encontrado, classifique:

| Prioridade | Critério |
|-----------|---------|
| **P0 — Risco de produção** | Pode causar incidente se não corrigido |
| **P1 — Bloqueia evolução** | Impede ou dificulta mudanças futuras |
| **P2 — Custo operacional** | Aumenta tempo de debug, onboarding ou manutenção |
| **P3 — Melhoria** | Nice-to-have sem impacto imediato |

### 3. Output
Entregue uma tabela priorizada:

| # | Prioridade | Local | Descrição | Esforço estimado |
|---|-----------|-------|-----------|-----------------|
| 1 | P0 | arquivo:linha | ... | pequeno/médio/grande |

Com recomendação de quais itens atacar primeiro e por quê.

## Agentes disponíveis (para análise profunda)
- Pragmatismo e manutenibilidade: `tech-lead-reviewer`
- Arquitetura: `architect-reviewer`
- Segurança: `security-reviewer`
- Dependências: `dependency-versions-reviewer`

## Escopo
$ARGUMENTS
