# Dependency Upgrade — Safe Process

Processo seguro para atualizar dependências.

## Antes de atualizar

### 1. Inventário
- Liste todas as dependências atuais e suas versões
- Identifique quais têm vulnerabilidades (`npm audit`, `pip-audit`, `mvn dependency-check`, `govulncheck`)
- Identifique quais estão desatualizadas

### 2. Priorização
| Prioridade | Critério |
|-----------|---------|
| P0 | Vulnerabilidade CRITICAL/HIGH conhecida |
| P1 | Dependência em EOL (sem patches de segurança) |
| P2 | Major version atrás (pode ter breaking changes acumulados) |
| P3 | Minor/patch updates (geralmente seguro) |

### 3. Verificação da nova versão
- É GA? (não RC, Alpha, Beta, SNAPSHOT)
- Tem changelog? Quais são os breaking changes?
- É compatível com o runtime? (Java 25, Python 3.13, Go 1.24, Node 22)
- Tem issues conhecidos na nova versão?

## Durante a atualização

### Uma dependência por vez
- Atualizar, rodar testes, commitar
- Nunca atualizar 10 dependências no mesmo commit
- Se algo quebrar, fica claro qual update causou

### Para major updates (breaking changes)
1. Ler changelog/migration guide completo
2. Identificar todas as breaking changes que afetam o projeto
3. Aplicar migração
4. Rodar todos os testes
5. Testar manualmente fluxos críticos

## Por ecossistema

### Java (Maven/Gradle)
```bash
# Ver dependências desatualizadas
mvn versions:display-dependency-updates
# Verificar vulnerabilidades
mvn org.owasp:dependency-check-maven:check
```

### Python
```bash
# Ver desatualizadas
pip list --outdated
# Verificar vulnerabilidades
pip-audit
```

### Go
```bash
# Ver desatualizadas
go list -m -u all
# Verificar vulnerabilidades
govulncheck ./...
```

### Node.js
```bash
# Ver desatualizadas
npm outdated
# Verificar vulnerabilidades
npm audit
```

### Terraform
```bash
# Ver providers desatualizados
terraform providers lock -platform=linux_amd64
# Verificar versão atual vs disponível
terraform version
```

## Checklist
- [ ] Versão é GA (não RC/Alpha/Beta)?
- [ ] Changelog lido para breaking changes?
- [ ] Compatível com runtime atual?
- [ ] Testes passando após update?
- [ ] Uma dependência por commit?
- [ ] Vulnerabilidades resolvidas?
