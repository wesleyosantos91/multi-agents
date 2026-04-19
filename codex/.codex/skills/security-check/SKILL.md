---
name: security-check
description: Revisão de segurança focada em superfície de ataque e hardening.
---

# Skill: security-check

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
Acione o `security-reviewer` para uma análise de segurança focada.

## Escopo
- Se `$ARGUMENTS` estiver vazio, analise os arquivos alterados na branch atual (`git diff main...HEAD`)
- Se `$ARGUMENTS` contiver um caminho ou módulo, foque nele

## O que verificar
- Autenticação e autorização
- Segredos hardcoded
- Dados sensíveis em logs
- Hardening de bordas
- Superfícies de abuso
- OWASP Top 10 aplicáveis
- Riscos críticos para produção

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

