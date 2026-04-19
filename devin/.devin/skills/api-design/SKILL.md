---
name: api-design
description: "Design de API REST seguindo boas práticas. Use quando pedirem para projetar API, definir endpoints, criar contrato REST ou OpenAPI."
argument-hint: "[contexto adicional]"
---

# API Design — REST Best Practices

Projete ou revise uma API REST seguindo boas práticas consolidadas.

## Princípios

### URLs
- Substantivos no plural: `/orders`, `/users`, `/payments`
- Hierarquia para relações: `/users/{id}/orders`
- Sem verbos na URL (use HTTP methods): `POST /orders` não `POST /createOrder`
- Kebab-case para multi-word: `/order-items`
- Máximo 3 níveis de aninhamento

### HTTP Methods
| Method | Semântica | Idempotente | Body |
|--------|-----------|-------------|------|
| GET | Ler recurso(s) | Sim | Não |
| POST | Criar recurso | Não | Sim |
| PUT | Substituir recurso inteiro | Sim | Sim |
| PATCH | Atualizar parcialmente | Não* | Sim |
| DELETE | Remover recurso | Sim | Não |

### Status Codes
| Código | Quando usar |
|--------|------------|
| 200 | Sucesso com body |
| 201 | Recurso criado (POST) — incluir `Location` header |
| 204 | Sucesso sem body (DELETE, PUT) |
| 400 | Input inválido — detalhar o que está errado |
| 401 | Não autenticado |
| 403 | Autenticado mas sem permissão |
| 404 | Recurso não encontrado |
| 409 | Conflito (duplicata, estado inválido) |
| 422 | Validação de negócio falhou |
| 429 | Rate limit excedido |
| 500 | Erro interno — nunca expor stack trace |

### Paginação
```json
GET /orders?page=1&size=20&sort=createdAt,desc

{
  "content": [...],
  "page": { "number": 1, "size": 20, "totalElements": 150, "totalPages": 8 }
}
```

### Erros (RFC 9457 — Problem Details)
```json
{
  "type": "https://api.example.com/errors/insufficient-funds",
  "title": "Insufficient Funds",
  "status": 422,
  "detail": "Account balance is 30.00 but transfer requires 50.00",
  "instance": "/transfers/txn-123"
}
```

### Filtros
- Query parameters para filtros simples: `?status=PENDING&minAmount=100`
- Operadores quando necessário: `?createdAfter=2024-01-01`
- Não inventar DSL de query complexa — se precisar, considere GraphQL

### Versionamento
- Preferir evolução backward-compatible (adicionar campos, nunca remover)
- Se inevitável: URL path (`/v2/orders`) ou header (`Accept-Version: 2`)

## Output
Quando projetando API, entregue:
1. Tabela de endpoints (method, URL, descrição, auth)
2. Request/response examples para cada endpoint
3. Códigos de erro esperados
4. Notas sobre paginação, filtros, ordenação
