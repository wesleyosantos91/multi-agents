---
name: security-audit
description: "Auditoria de segurança rápida em código ou projeto. Use quando pedirem para verificar segurança, encontrar vulnerabilidades ou auditar código."
---

# Security Audit

Realize uma auditoria de segurança focada no código ou projeto especificado.

## Verificações por categoria

### 1. Segredos e credenciais
- Grep por padrões de segredos: `password`, `secret`, `api_key`, `token`, `credential`, `private_key`
- Verificar `.env` versionado no git
- Verificar hardcoded strings que parecem credenciais
- Verificar variáveis de ambiente com valores default sensíveis

### 2. Injection
- SQL: concatenação de strings em queries (`"SELECT * FROM " + input`)
- Command: input em `exec`, `system`, `subprocess`, `os/exec`
- XSS: input renderizado sem sanitização em HTML
- Path traversal: input em operações de arquivo sem validação
- Deserialização insegura: `pickle`, `yaml.load`, `ObjectInputStream`

### 3. Autenticação e autorização
- Endpoints sem autenticação que deveriam ter
- Verificações de autorização faltando (IDOR)
- Tokens em localStorage (deveria ser httpOnly cookie)
- Sessões sem expiração

### 4. Dados sensíveis
- Dados pessoais em logs (PII)
- Stack traces expostos em respostas de erro
- Informações internas em mensagens de erro
- Dados sensíveis em URLs (query parameters)

### 5. Dependências
- Verificar vulnerabilidades conhecidas (quando possível rodar audit)
- Dependências sem manutenção ativa
- Versões muito antigas

### 6. Configuração
- Debug mode em produção
- CORS permissivo (`*`)
- Headers de segurança ausentes
- TLS/HTTPS não enforçado

## Output

### Severidade
- **CRITICAL**: exploração imediata possível, dados em risco
- **HIGH**: vulnerabilidade exploável com esforço moderado
- **MEDIUM**: risco real mas mitigado por outros controles
- **LOW**: melhoria de hardening, defesa em profundidade
- **INFO**: observação sem risco imediato

### Formato
```
[CRITICAL] arquivo:linha — descrição + como explorar + como corrigir
[HIGH] arquivo:linha — descrição + impacto + correção
[MEDIUM] arquivo:linha — descrição + correção
[LOW] arquivo:linha — descrição + sugestão
```

### Resumo final
- Total de achados por severidade
- Top 3 ações prioritárias
- Veredicto: SEGURO / ATENÇÃO / RISCO CRÍTICO
