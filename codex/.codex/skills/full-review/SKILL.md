---
name: full-review
description: Revisão Nível 4, completa e transversal, para mudanças não triviais.
---

# Skill: full-review

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
Acione o `staff-engineer-orchestrator` para uma revisão COMPLETA (Nível 4) do projeto ou branch.

## Instrução
Execute a pipeline completa de revisão com TODOS os agentes relevantes, na ordem definida no CLAUDE.md.

## Passos obrigatórios
1. `git diff main...HEAD` para entender todas as mudanças
2. Classifique como Nível 4 (pipeline completa)
3. Acione TODOS os agentes relevantes conforme a stack detectada
4. Use o formato completo de 26 seções
5. Consolide achados, resolva conflitos, entregue plano final priorizado

## O que é esperado
- Diagnóstico completo
- Achados de cada agente acionado
- Conflitos entre recomendações resolvidos
- Plano final priorizado com justificativa
- Diff sugerido
- Riscos remanescentes
- Estratégia de validação

## Contexto adicional
$ARGUMENTS


## Critérios de qualidade
- Evidências explícitas (arquivos, símbolos, comandos, testes).
- Riscos classificados por severidade.
- Escopo controlado e sem refatoração lateral não solicitada.

## Regras de proteção
- Preferir menor mudança defensável.
- Não inferir versões por memória quando houver dependências.
- Não omitir limitações de validação.

