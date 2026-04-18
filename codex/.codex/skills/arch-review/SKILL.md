---
name: arch-review
description: Revisão arquitetural focada em boundaries, resiliência e trade-offs.
---

# Skill: arch-review

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
Acione o `architect-reviewer` para uma análise arquitetural focada.

## Escopo
- Se `$ARGUMENTS` estiver vazio, analise a arquitetura do projeto ou branch atual
- Se `$ARGUMENTS` contiver um módulo ou decisão, foque nele

## O que avaliar
- Boundaries entre camadas
- Acoplamento e coesão
- Trade-offs técnicos
- Resiliência e tolerância a falhas
- Decisão de modelo de execução (Lambda vs container vs batch vs Step Functions)
- Compatibilidade evolutiva de contratos
- Separação correta: web/ (borda síncrona), message/ (borda assíncrona), domain/, infrastructure/, core/

## Entrada do usuário
$ARGUMENTS


## Critérios de qualidade
- Evidências explícitas (arquivos, símbolos, comandos, testes).
- Riscos classificados por severidade.
- Escopo controlado e sem refatoração lateral não solicitada.

## Regras de proteção
- Preferir menor mudança defensável.
- Não inferir versões por memória quando houver dependências.
- Não omitir limitações de validação.

