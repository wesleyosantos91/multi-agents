---
name: cicd-review
description: "Acione o `cicd-pipeline-engineer` para análise de pipelines CI/CD."
argument-hint: "[contexto adicional]"
---

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
