---
name: tech-debt
description: Identificação e priorização de débito técnico.
---

# Skill: tech-debt

## Quando dispara
- Quando o usuário solicitar explicitamente o workflow $name.
- Quando o contexto da tarefa for compatível com o objetivo descrito nesta skill.

## Quando NÃO dispara
- Quando a tarefa exigir outro workflow mais específico do catálogo.
- Quando o escopo não tiver relação com o objetivo técnico desta skill.

## Inputs esperados
- Contexto da demanda.
- Escopo ou módulo alvo (quando aplicável).
- Restrições técnicas e de risco.

## Saída esperada
- Diagnóstico objetivo com evidências.
- Recomendação acionável e priorizada.
- Plano de validação proporcional ao risco.

## Workflow passo a passo
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


## Critérios de qualidade
- Evidências explícitas (arquivos, símbolos, comandos, testes).
- Riscos classificados por severidade.
- Escopo controlado e sem refatoração lateral não solicitada.

## Regras de proteção
- Preferir menor mudança defensável.
- Não inferir versões por memória quando houver dependências.
- Não omitir limitações de validação.

