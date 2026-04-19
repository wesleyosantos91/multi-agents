---
description: "Prompt reutilizavel do fluxo finops para Copilot Chat."
---

Acione o `finops-reviewer` para análise de custo AWS do projeto ou módulo especificado.

## O que verificar
- Retenção de logs CloudWatch
- Rightsizing de instâncias/containers
- Tags de custo (cost allocation tags) nos resources Terraform
- Anti-padrões de billing (NAT Gateway desnecessário, logs ilimitados, provisionamento excessivo)
- Uso eficiente de serviços gerenciados
- Reservas e savings plans quando aplicável
- Riscos de surpresa financeira em produção

## Escopo
- Se `{{ARGUMENTS}}` estiver vazio, analise todo o IaC (iac/terraform/) e configurações AWS
- Se `{{ARGUMENTS}}` contiver um caminho, foque nele

## Entrada do usuário
{{ARGUMENTS}}

