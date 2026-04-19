---
name: health-check
description: "Execute um diagnóstico rápido de saúde do projeto ou módulo especificado."
argument-hint: "[contexto adicional]"
---

Execute um diagnóstico rápido de saúde do projeto ou módulo especificado.

## Verificações obrigatórias

### 1. Build
- O projeto compila/builda sem erros? (mvn compile, go build, pip install -e, npm run build — conforme stack)

### 2. Testes
- Os testes passam? Rode a suite de testes do módulo
- Quantos testes existem? Há cobertura razoável?

### 3. Dependências
- Há vulnerabilidades conhecidas? (mvn dependency-check, pip-audit, govulncheck, npm audit — conforme stack)
- Há dependências desatualizadas criticamente?

### 4. Código
- Há TODOs/FIXMEs/HACKs no código? (Grep rápido)
- Há arquivos com segredos hardcoded? (.env versionado, senhas em config)
- Lint passa sem erros críticos?

### 5. Infraestrutura
- docker-compose sobe sem erros?
- Terraform valida? (terraform validate, se aplicável)

## Output
Entregue um relatório compacto:

| Área | Status | Detalhes |
|------|--------|----------|
| Build | OK/FALHA | ... |
| Testes | OK/FALHA | X passando, Y falhando |
| Deps | OK/ATENÇÃO | vulnerabilidades encontradas |
| Código | OK/ATENÇÃO | TODOs, segredos, lint |
| Infra | OK/FALHA | docker, terraform |

**Veredicto final**: SAUDÁVEL / ATENÇÃO / CRÍTICO

## Agentes disponíveis (para diagnóstico profundo)
- Build/testes: `qa-quality-engineer`
- Dependências: `dependency-versions-reviewer`
- Infra/docker: `sre-platform-engineer`
- Segurança: `security-reviewer`

## Escopo
$ARGUMENTS
