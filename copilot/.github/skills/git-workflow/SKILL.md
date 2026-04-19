---
name: git-workflow
description: Skill importada do EXEMPLO (git-workflow.md).
allowed-tools: "read,search"
user-invocable: true
---

# Skill

---
name: git-workflow
description: "Auxilia em operações git: resolver conflitos, rebase, cherry-pick, bisect, recuperar trabalho. Use quando pedirem ajuda com git, merge conflicts ou histórico."
---

# Git Workflow Helper

Auxilia em operações git comuns e complexas.

## Operações disponíveis

### Resolver merge conflicts
1. `git diff --name-only --diff-filter=U` para listar arquivos em conflito
2. Ler cada arquivo com conflito
3. Entender a intenção de ambos os lados (ours vs theirs)
4. Propor resolução preservando a intenção correta
5. Nunca resolver conflito descartando mudanças sem confirmar

### Rebase interativo (simulado)
1. `git log main...HEAD --oneline` para ver commits
2. Sugerir squash, reorder ou reword
3. Executar com comandos não-interativos quando possível

### Cherry-pick
1. Identificar o commit correto
2. `git cherry-pick <sha>` 
3. Se conflitar, resolver e continuar

### Bisect (encontrar commit que introduziu bug)
1. `git log --oneline -20` para contexto
2. Guiar o usuário: "Este commit tem o bug? (sim/não)"
3. Ou automatizar com `git bisect run <test-command>`

### Recuperar trabalho perdido
- `git reflog` para encontrar commits "perdidos"
- `git stash list` para stashes esquecidos
- `git log --all --graph --oneline` para visualizar branches

### Branch cleanup
- Listar branches mergeadas: `git branch --merged main`
- Sugerir exclusão de branches já mergeadas
- Nunca deletar branch sem confirmar

## Regras
- **Nunca force push sem confirmar** — pode perder trabalho de outros
- **Nunca reset --hard sem confirmar** — pode perder trabalho local
- **Preferir revert a reset** quando commits já foram pushed
- **Sempre verificar** em qual branch está antes de operar
- Explicar o que cada comando faz antes de executar
