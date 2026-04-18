---
name: health-check
description: Diagnóstico rápido de saúde técnica do projeto.
---

# Skill: health-check

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


## Critérios de qualidade
- Evidências explícitas (arquivos, símbolos, comandos, testes).
- Riscos classificados por severidade.
- Escopo controlado e sem refatoração lateral não solicitada.

## Regras de proteção
- Preferir menor mudança defensável.
- Não inferir versões por memória quando houver dependências.
- Não omitir limitações de validação.

