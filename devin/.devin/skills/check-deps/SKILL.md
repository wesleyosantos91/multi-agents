---
name: check-deps
description: "Acione o `dependency-versions-reviewer` para validar todas as dependências do projeto ou módulo especificado."
argument-hint: "[contexto adicional]"
---

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
