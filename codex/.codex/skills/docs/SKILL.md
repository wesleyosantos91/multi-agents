---
name: docs
description: Criação/manutenção de documentação técnica operacional.
---

# Skill: docs

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
Acione o `tech-writer` para revisar, criar ou atualizar documentação técnica.

## Escopo
- Se `$ARGUMENTS` contiver "review" ou estiver vazio, faça diagnóstico da documentação existente
- Se `$ARGUMENTS` contiver "create", crie a documentação faltante
- Se `$ARGUMENTS` contiver um componente ou fluxo, documente especificamente ele

## O que o tech-writer faz
1. Lê o repositório antes de documentar (nunca inventa comandos)
2. Diagnostica estado atual da documentação
3. Cria ou atualiza: README, getting-started, local-development, testing, troubleshooting, project-structure
4. Cria ADRs quando há decisões arquiteturais não documentadas
5. Reporta lacunas que exigem validação humana

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

