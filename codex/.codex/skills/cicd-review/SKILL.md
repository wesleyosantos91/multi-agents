---
name: cicd-review
description: Revisão de pipeline CI/CD e quality gates.
---

# Skill: cicd-review

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
Acione o `cicd-pipeline-engineer` para análise de pipelines CI/CD.

## Escopo
- Se `$ARGUMENTS` estiver vazio, analise todos os workflows em `.github/workflows/`
- Se `$ARGUMENTS` contiver um workflow ou estratégia de deploy, foque nele

## O que avaliar
- GitHub Actions: estrutura de jobs, cache, paralelização, secrets
- Deploy strategy Lambda: versions/aliases, blue/green, canary
- Terraform em CI: plan em PR, apply em merge, state management
- Quality gates: lint, test, scan, build
- Rollback automatizado via CodeDeploy + CloudWatch Alarm
- OIDC para AWS (sem credenciais de longa duração)
- Promoção entre ambientes (dev → staging → prod)

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

