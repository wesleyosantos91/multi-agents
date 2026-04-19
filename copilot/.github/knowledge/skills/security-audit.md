---
name: security-audit
description: "Auditoria de segurança e padrões de autenticação/autorização: audit checklist, OAuth2/OIDC, JWT, API keys, RBAC/ABAC, secrets management. Use quando verificar segurança, auditar código, ou implementar auth."
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

---

# Authentication & Authorization Patterns

Padroes de implementacao de auth para sistemas criticos.

## OAuth2 / OIDC Flows

| Flow | Quando usar |
|------|-------------|
| **Authorization Code + PKCE** | SPA, mobile, server-side web |
| **Client Credentials** | Service-to-service (M2M) |
| **Device Authorization** | CLI, TV, IoT |

**Nunca usar**: Implicit flow (deprecated), Resource Owner Password.

## JWT Validation

### Java (Spring Security)
```java
@Bean
public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
    return http
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/actuator/health").permitAll()
            .requestMatchers("/api/admin/**").hasRole("ADMIN")
            .requestMatchers("/api/**").authenticated()
            .anyRequest().denyAll()
        )
        .oauth2ResourceServer(oauth2 -> oauth2
            .jwt(jwt -> jwt.jwtAuthenticationConverter(jwtConverter()))
        )
        .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
        .csrf(AbstractHttpConfigurer::disable)
        .build();
}

// Extrair roles do JWT
@Bean
public JwtAuthenticationConverter jwtConverter() {
    var grantedAuthorities = new JwtGrantedAuthoritiesConverter();
    grantedAuthorities.setAuthoritiesClaimName("roles");
    grantedAuthorities.setAuthorityPrefix("ROLE_");
    var converter = new JwtAuthenticationConverter();
    converter.setJwtGrantedAuthoritiesConverter(grantedAuthorities);
    return converter;
}
```

### Python (FastAPI + python-jose)
```python
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
) -> TokenPayload:
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.jwt_public_key,
            algorithms=["RS256"],
            audience=settings.jwt_audience,
            issuer=settings.jwt_issuer,
        )
        return TokenPayload(**payload)
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/api/orders")
async def list_orders(user: TokenPayload = Depends(get_current_user)):
    ...
```

### Go (middleware JWT)
```go
func JWTMiddleware(keySet jwk.Set, issuer, audience string) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            token := strings.TrimPrefix(r.Header.Get("Authorization"), "Bearer ")
            if token == "" {
                http.Error(w, "missing token", http.StatusUnauthorized)
                return
            }
            parsed, err := jwt.Parse([]byte(token),
                jwt.WithKeySet(keySet),
                jwt.WithIssuer(issuer),
                jwt.WithAudience(audience),
            )
            if err != nil {
                http.Error(w, "invalid token", http.StatusUnauthorized)
                return
            }
            ctx := context.WithValue(r.Context(), userKey, parsed)
            next.ServeHTTP(w, r.WithContext(ctx))
        })
    }
}
```

## API Key Authentication

Para service-to-service simples ou integrações externas:

```java
// Java — Filter
@Component
public class ApiKeyFilter extends OncePerRequestFilter {
    @Value("${api.keys}") private Set<String> validKeys;

    @Override
    protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res,
                                     FilterChain chain) throws ServletException, IOException {
        String key = req.getHeader("X-API-Key");
        if (key == null || !validKeys.contains(key)) {
            res.sendError(HttpServletResponse.SC_UNAUTHORIZED);
            return;
        }
        chain.doFilter(req, res);
    }
}
```

- Armazenar chaves como hash (SHA-256), nao plaintext
- Rotacao periodica obrigatoria
- Rate limiting por chave
- Logging de uso por chave (auditoria)

## RBAC vs ABAC

| Modelo | Quando usar | Exemplo |
|--------|-------------|---------|
| **RBAC** (Role-Based) | Permissoes fixas por papel | ADMIN, MANAGER, USER |
| **ABAC** (Attribute-Based) | Permissoes dinamicas por contexto | "owner do recurso", "mesmo departamento" |

### RBAC — Java
```java
@PreAuthorize("hasRole('ADMIN')")
@DeleteMapping("/api/orders/{id}")
public void deleteOrder(@PathVariable String id) { service.delete(id); }

@PreAuthorize("hasAnyRole('ADMIN', 'MANAGER')")
@PutMapping("/api/orders/{id}")
public Order updateOrder(@PathVariable String id, @RequestBody OrderRequest req) { ... }
```

### ABAC — Owner check
```java
@PreAuthorize("@orderSecurity.isOwner(#id, authentication)")
@GetMapping("/api/orders/{id}")
public Order getOrder(@PathVariable String id) { ... }

@Component("orderSecurity")
public class OrderSecurity {
    public boolean isOwner(String orderId, Authentication auth) {
        var order = repository.findById(orderId).orElseThrow();
        return order.getCustomerId().equals(auth.getName());
    }
}
```

### ABAC — Python
```python
async def require_owner(order_id: str, user: TokenPayload = Depends(get_current_user)):
    order = await repository.find(order_id)
    if order.customer_id != user.sub:
        raise HTTPException(status_code=403, detail="Not resource owner")
    return order

@app.get("/api/orders/{order_id}")
async def get_order(order: Order = Depends(require_owner)):
    return order
```

## Auth Checklist
- [ ] JWT com validacao completa (signature, exp, iss, aud)?
- [ ] Tokens stateless (sem session server-side)?
- [ ] Refresh token rotation implementado?
- [ ] API keys armazenadas como hash?
- [ ] Endpoints publicos explicitamente listados (allowlist, nao denylist)?
- [ ] RBAC ou ABAC consistente em todos os endpoints?
- [ ] Audit log para acoes administrativas?
- [ ] Rate limiting por usuario/chave?
- [ ] CORS restrito a origens conhecidas?
- [ ] Secrets (JWT keys, API keys) via Secrets Manager, nao env vars?
