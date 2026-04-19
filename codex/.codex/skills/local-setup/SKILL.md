---
name: local-setup
description: Validação e melhoria de setup local e onboarding.
---

# Skill: local-setup

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
Acione o `devex-reviewer` para validar o ambiente de desenvolvimento local.

## O que verificar
- docker-compose.yml sobe todos os serviços necessários
- Ministack (porta 4566) está configurado e acessível
- application-local.yml ou equivalente está completo e funcional
- Makefile tem targets claros (build, test, deploy, local)
- Onboarding é possível em 3-5 comandos máximo
- Dev Container está configurado (se existir .devcontainer/)

## Escopo
- Se `$ARGUMENTS` estiver vazio, valide o projeto inteiro
- Se `$ARGUMENTS` contiver um módulo, foque nele

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

