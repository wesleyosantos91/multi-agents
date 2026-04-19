---
name: finops
description: Revisão de custo cloud com trade-offs de resiliência.
---

# Skill: finops

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
- Se `$ARGUMENTS` estiver vazio, analise todo o IaC (iac/terraform/) e configurações AWS
- Se `$ARGUMENTS` contiver um caminho, foque nele

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

