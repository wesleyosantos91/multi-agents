---
name: compliance
description: Revisão de conformidade regulatória e proteção de dados.
---

# Skill: compliance

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
Acione o `compliance-reviewer` para análise de conformidade regulatória.

## O que verificar
- Dados pessoais mapeados (LGPD/GDPR)
- Base legal para tratamento identificada
- Dados pessoais ausentes de logs, traces e métricas
- Residência de dados alinhada com região AWS (sa-east-1 para Brasil)
- Retenção e descarte de dados pessoais definidos
- Consentimento e direitos do titular
- Anonimização quando aplicável

## Escopo
- Se `$ARGUMENTS` estiver vazio, analise todo o projeto
- Se `$ARGUMENTS` contiver um módulo ou fluxo, foque nele

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

