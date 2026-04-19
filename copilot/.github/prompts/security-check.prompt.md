---
description: "Prompt reutilizavel do fluxo security-check para Copilot Chat."
---

Acione o `security-reviewer` para uma análise de segurança focada.

## Escopo
- Se `{{ARGUMENTS}}` estiver vazio, analise os arquivos alterados na branch atual (`git diff main...HEAD`)
- Se `{{ARGUMENTS}}` contiver um caminho ou módulo, foque nele

## O que verificar
- Autenticação e autorização
- Segredos hardcoded
- Dados sensíveis em logs
- Hardening de bordas
- Superfícies de abuso
- OWASP Top 10 aplicáveis
- Riscos críticos para produção

## Entrada do usuário
{{ARGUMENTS}}

