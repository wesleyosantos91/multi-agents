---
name: check-deps
description: Validação de versões de dependências e runtimes com foco em GA e segurança.
---

# Skill: check-deps

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
Acione o `dependency-versions-reviewer` para validar todas as dependências do projeto ou módulo especificado.

## Regras
- Use WebSearch para verificar versões — NUNCA assuma por memória
- Valide que cada dependência é GA (não RC, SNAPSHOT, M1, Alpha, Beta)
- Confirme compatibilidade com Java 25 quando aplicável
- Verifique CVEs críticos ou altos conhecidos
- Verifique EOL declarado
- Inclua Terraform providers e Docker base images

## Escopo
- Se `$ARGUMENTS` estiver vazio, busque todos os arquivos de dependência no projeto (pom.xml, build.gradle, pyproject.toml, go.mod, requirements*.txt, package.json, Terraform *.tf)
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

