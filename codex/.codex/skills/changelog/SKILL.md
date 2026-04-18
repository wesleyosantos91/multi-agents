---
name: changelog
description: Geração de changelog estruturado por tipo de mudança.
---

# Skill: changelog

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
Gere um changelog das mudanças da branch atual comparada com main.

## Processo

### 1. Coleta
- `git log main...HEAD --oneline` para listar todos os commits
- `git diff main...HEAD --stat` para listar arquivos alterados
- Leia os diffs relevantes para entender a natureza das mudanças

### 2. Classificação
Classifique cada mudança:
- **feat**: nova funcionalidade
- **fix**: correção de bug
- **refactor**: mudança interna sem impacto funcional
- **docs**: documentação
- **test**: testes
- **infra**: CI/CD, IaC, Docker, configuração
- **deps**: atualização de dependências
- **breaking**: mudança que quebra compatibilidade

### 3. Output

```markdown
## Changelog

### Features
- feat: descrição da feature

### Fixes
- fix: descrição do fix

### Breaking Changes
- breaking: o que mudou e o impacto

### Other
- refactor/docs/test/infra/deps: descrição
```

## Agente
Se o changelog for para PR ou release, considere acionar `tech-writer` para revisar a documentação.

## Contexto adicional
$ARGUMENTS


## Critérios de qualidade
- Evidências explícitas (arquivos, símbolos, comandos, testes).
- Riscos classificados por severidade.
- Escopo controlado e sem refatoração lateral não solicitada.

## Regras de proteção
- Preferir menor mudança defensável.
- Não inferir versões por memória quando houver dependências.
- Não omitir limitações de validação.

