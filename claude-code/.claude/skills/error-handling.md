---
name: error-handling
description: "Guia de tratamento de erros por linguagem. Use quando pedirem para melhorar error handling, tratar exceções, ou padronizar erros em API."
---

# Error Handling — Best Practices

Guia de tratamento de erros correto por linguagem e contexto.

## Princípios universais

1. **Falhe rápido**: detecte erros o mais cedo possível
2. **Falhe claramente**: mensagens de erro devem dizer o que aconteceu e o que fazer
3. **Não engula erros**: catch vazio é bug — log ou propague
4. **Separe erros de negócio de erros técnicos**: tratamento diferente
5. **Não exponha detalhes internos**: stack traces e paths são para logs, não para respostas

## Por linguagem

### Java
```java
// Erros de negócio → exceções checked ou runtime específicas
public class InsufficientStockException extends BusinessException {
    public InsufficientStockException(String productId, int requested, int available) {
        super("Product %s: requested %d but only %d available"
            .formatted(productId, requested, available));
    }
}

// Handler global → resposta padronizada
@ExceptionHandler(BusinessException.class)
ResponseEntity<ProblemDetail> handle(BusinessException ex) {
    var problem = ProblemDetail.forStatusAndDetail(
        HttpStatus.UNPROCESSABLE_ENTITY, ex.getMessage());
    return ResponseEntity.status(422).body(problem);
}
```

### Python
```python
# Exceções de domínio
class InsufficientStockError(DomainError):
    def __init__(self, product_id: str, requested: int, available: int):
        super().__init__(
            f"Product {product_id}: requested {requested} but only {available} available"
        )

# Handler — nunca expor traceback
@app.exception_handler(DomainError)
async def domain_error_handler(request, exc):
    return JSONResponse(status_code=422, content={"detail": str(exc)})
```

### Go
```go
// Erros tipados para negócio
type InsufficientStockError struct {
    ProductID string
    Requested int
    Available int
}

func (e *InsufficientStockError) Error() string {
    return fmt.Sprintf("product %s: requested %d but only %d available",
        e.ProductID, e.Requested, e.Available)
}

// Sempre checar erros — nunca ignorar
result, err := service.PlaceOrder(ctx, order)
if err != nil {
    var stockErr *InsufficientStockError
    if errors.As(err, &stockErr) {
        // erro de negócio — resposta 422
    }
    // erro técnico — resposta 500 + log
    return fmt.Errorf("placing order: %w", err)
}
```

## Em APIs — Resposta padronizada

### RFC 9457 (Problem Details)
```json
{
  "type": "https://api.example.com/errors/insufficient-stock",
  "title": "Insufficient Stock",
  "status": 422,
  "detail": "Product PRD-123: requested 10 but only 5 available",
  "instance": "/orders/ord-456"
}
```

### Mapping de erros
| Tipo de erro | HTTP Status | Log level |
|-------------|-------------|-----------|
| Validação de input | 400 | WARN |
| Não autenticado | 401 | WARN |
| Sem permissão | 403 | WARN |
| Não encontrado | 404 | DEBUG |
| Regra de negócio | 422 | INFO |
| Rate limit | 429 | WARN |
| Erro interno | 500 | ERROR |
| Dependência falhou | 502/503 | ERROR |

## Anti-patterns
- `catch (Exception e) {}` — engolir erros
- `throw new RuntimeException("error")` — mensagem genérica
- Log + rethrow do mesmo erro (duplica logs)
- Stack trace em resposta HTTP
- Usar exceções para controle de fluxo normal
- `panic` em Go (exceto inicialização)
