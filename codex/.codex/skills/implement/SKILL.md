---
name: implement
description: Análise e implementação orientada por orquestração com menor mudança defensável.
---

# Skill: implement

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
Acione o `staff-engineer-orchestrator` para analisar e implementar a demanda descrita abaixo.

## Regras
- NUNCA implemente sem análise adequada
- Siga a ordem de consulta de agentes definida no CLAUDE.md
- Se houver dependências (pom.xml, build.gradle, go.mod, pyproject.toml, Terraform providers), o `dependency-versions-reviewer` DEVE ser acionado antes do `software-engineer`
- Entregue a menor implementação correta, sustentável e profissional

## Demanda
$ARGUMENTS


## Critérios de qualidade
- Evidências explícitas (arquivos, símbolos, comandos, testes).
- Riscos classificados por severidade.
- Escopo controlado e sem refatoração lateral não solicitada.

## Regras de proteção
- Preferir menor mudança defensável.
- Não inferir versões por memória quando houver dependências.
- Não omitir limitações de validação.

