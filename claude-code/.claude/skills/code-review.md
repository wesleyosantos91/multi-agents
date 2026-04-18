---
name: code-review
description: "Revisão de código estruturada com checklist de qualidade, segurança e manutenibilidade. Use quando pedirem para revisar código, PR ou branch."
---

# Code Review Estruturado

Realize uma revisão de código completa e estruturada.

## Processo

### 1. Contexto
- Identifique os arquivos alterados (`git diff main...HEAD --stat` ou o escopo indicado)
- Entenda o propósito da mudança (commit messages, PR description, contexto do usuário)
- Identifique a linguagem e framework envolvidos

### 2. Checklist de revisão

#### Correção
- [ ] O código faz o que deveria fazer?
- [ ] Edge cases tratados?
- [ ] Erros tratados adequadamente?
- [ ] Sem regressões introduzidas?

#### Segurança
- [ ] Sem segredos hardcoded?
- [ ] Input validado em bordas?
- [ ] Sem injection (SQL, command, XSS)?
- [ ] Sem dados sensíveis em logs?

#### Qualidade
- [ ] Código legível e compreensível?
- [ ] Nomes claros e consistentes?
- [ ] Sem duplicação desnecessária?
- [ ] Sem complexidade desnecessária?
- [ ] Idiomatismo da linguagem respeitado?

#### Testes
- [ ] Testes existem para o código novo?
- [ ] Testes cobrem happy path e edge cases?
- [ ] Testes existentes continuam passando?

#### Manutenibilidade
- [ ] Fácil de entender para outro desenvolvedor?
- [ ] Fácil de modificar no futuro?
- [ ] Sem acoplamento desnecessário?

### 3. Output

Para cada achado, classifique:
- **BLOCKER**: deve corrigir antes de merge
- **WARNING**: deveria corrigir, não bloqueia
- **SUGGESTION**: melhoria opcional
- **PRAISE**: algo bem feito (reconheça boas práticas)

Formato:
```
[BLOCKER] arquivo:linha — descrição do problema e sugestão de correção
[WARNING] arquivo:linha — descrição
[SUGGESTION] arquivo:linha — descrição
[PRAISE] arquivo:linha — o que está bem feito
```

### 4. Veredicto final
- **APPROVE**: pode mergear
- **REQUEST CHANGES**: tem blockers que precisam ser resolvidos
- **COMMENT**: sem blockers, mas há sugestões relevantes
