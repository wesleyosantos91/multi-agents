---
name: scaffold
description: Scaffolding de módulos seguindo padrões reais do repositório.
---

# Skill: scaffold

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
Crie a estrutura de um novo módulo/componente seguindo os padrões do projeto.

## Processo obrigatório

### 1. Detecção de padrões
- Leia a estrutura de módulos existentes no projeto (Glob + Read)
- Identifique convenções: nomes de pacotes, organização de pastas, configuração, testes
- Identifique o padrão de build (pom.xml, build.gradle, pyproject.toml, go.mod)

### 2. Scaffolding
- Crie a estrutura seguindo **exatamente** os padrões detectados
- Inclua: código principal, testes, configuração, build file
- Siga a arquitetura definida no CLAUDE.md (web/, message/, core/, domain/, infrastructure/)
- Use as versões de dependências já existentes no projeto — não invente versões

### 3. Validação
- Confirme que o build compila/importa sem erros
- Confirme que os testes do scaffold passam
- Confirme que a estrutura é consistente com os módulos existentes

### 4. Output
Entregue:
- **Arquivos criados**: lista completa
- **Padrões seguidos**: quais módulos existentes serviram de referência
- **Próximos passos**: o que o desenvolvedor precisa fazer para completar a implementação

## Agentes disponíveis (quando necessário)
- Se envolver dependências novas: acione `dependency-versions-reviewer` antes de criar
- Para a criação: use `software-engineer`
- Para validar aderência: acione `tech-lead-reviewer`

## O que criar
$ARGUMENTS


## Critérios de qualidade
- Evidências explícitas (arquivos, símbolos, comandos, testes).
- Riscos classificados por severidade.
- Escopo controlado e sem refatoração lateral não solicitada.

## Regras de proteção
- Preferir menor mudança defensável.
- Não inferir versões por memória quando houver dependências.
- Não omitir limitações de validação.

