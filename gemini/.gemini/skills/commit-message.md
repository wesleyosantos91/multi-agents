# Commit Message — Conventional Commits

Gere uma mensagem de commit seguindo Conventional Commits.

## Processo

1. Analise as mudanças staged (`git diff --cached`) ou todas as mudanças (`git diff`)
2. Identifique a natureza da mudança
3. Gere a mensagem seguindo o formato abaixo

## Formato

```
<type>(<scope>): <description>

[body opcional — explique o "por quê", não o "o quê"]

[footer opcional — breaking changes, referências]
```

### Types
- `feat`: nova funcionalidade
- `fix`: correção de bug
- `refactor`: mudança interna sem impacto funcional
- `docs`: documentação
- `test`: testes
- `chore`: build, CI, dependências, configuração
- `perf`: otimização de performance
- `style`: formatação (sem mudança de lógica)

### Regras
- `description` em inglês, imperativo, lowercase, sem ponto final, máximo 72 caracteres
- `scope` é opcional — use quando clarifica (ex: `feat(auth):`, `fix(orders):`)
- `body` só quando o "por quê" não é óbvio pela description
- `BREAKING CHANGE:` no footer quando há breaking change
- Uma mudança = um commit. Se são mudanças independentes, sugira commits separados

### Exemplos

```
feat(orders): add pagination to list orders endpoint

fix: handle null optional fields in payment payload

refactor(auth): extract token validation to dedicated service

Previously scattered across three controllers. Centralizing
reduces duplication and makes rotation easier.

chore(deps): bump spring-boot from 3.4.1 to 3.5.0

BREAKING CHANGE: minimum Java version is now 25
```
