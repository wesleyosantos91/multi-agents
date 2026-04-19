---
name: pr-description
description: Skill importada do EXEMPLO (pr-description.md).
allowed-tools: "read,search"
user-invocable: true
---

# Skill

---
name: pr-description
description: "Gera descrição de Pull Request estruturada. Use quando pedirem para criar PR, descrever PR ou preparar PR description."
---

# PR Description Generator

Gere uma descrição de Pull Request clara e estruturada.

## Processo

1. Analise todos os commits da branch (`git log main...HEAD --oneline`)
2. Analise todos os arquivos alterados (`git diff main...HEAD --stat`)
3. Leia os diffs para entender a natureza completa da mudança
4. Gere a descrição

## Formato

```markdown
## Summary
<!-- 1-3 frases descrevendo O QUE e POR QUÊ -->

## Changes
<!-- Lista de mudanças agrupadas por área -->
- **area**: descrição da mudança

## Breaking Changes
<!-- Só se houver — o que quebra e como migrar -->

## Test Plan
- [ ] Testes unitários passando
- [ ] Testes de integração passando
- [ ] Testado manualmente: [descrever cenários]

## Screenshots
<!-- Só se houver mudança visual -->

## Notes for Reviewers
<!-- Contexto adicional que ajuda na revisão -->
```

## Regras
- Summary foca no "por quê", não no "o quê" (o diff mostra o quê)
- Changes agrupados logicamente, não por arquivo
- Se o PR é grande demais (>500 linhas, >10 arquivos), sugira split
- Não liste todos os arquivos — agrupe por área funcional
- Linguagem: mesmo idioma do projeto (português ou inglês)
