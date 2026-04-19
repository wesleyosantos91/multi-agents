---
name: error-handling
description: "Guia de tratamento de erros e resiliência por linguagem: exceções, Problem Details RFC 9457, retry, circuit breaker, bulkhead, rate limiting. Use quando melhorar error handling, tratar exceções, padronizar erros em API, ou implementar resiliência."
argument-hint: "[contexto adicional]"
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

---

# Resilience Patterns

Padroes de resiliencia cross-language para sistemas criticos.

## Retry com backoff exponencial e jitter

### Java (Resilience4j)
```java
@Bean
public RetryConfig retryConfig() {
    return RetryConfig.custom()
        .maxAttempts(3)
        .waitDuration(Duration.ofMillis(500))
        .intervalFunction(IntervalFunction.ofExponentialRandomBackoff(
            Duration.ofMillis(500), 2.0, Duration.ofSeconds(10)))
        .retryOnException(e -> e instanceof TransientException)
        .ignoreExceptions(BusinessException.class)
        .build();
}

// Uso com annotation
@Retry(name = "orderService", fallbackMethod = "fallback")
public Order getOrder(String id) { return client.fetchOrder(id); }

private Order fallback(String id, Exception e) {
    log.warn("Fallback for order {}: {}", id, e.getMessage());
    return Order.empty(id);
}
```

### Python (tenacity)
```python
from tenacity import retry, stop_after_attempt, wait_exponential_jitter, retry_if_exception_type

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential_jitter(initial=0.5, max=10, jitter=2),
    retry=retry_if_exception_type(TransientError),
    before_sleep=lambda state: logger.warning(f"Retry {state.attempt_number}: {state.outcome.exception()}"),
)
async def fetch_order(order_id: str) -> Order:
    return await client.get(f"/orders/{order_id}")
```

### Go (custom — stdlib)
```go
func WithRetry[T any](ctx context.Context, maxAttempts int, fn func() (T, error)) (T, error) {
    var zero T
    for attempt := range maxAttempts {
        result, err := fn()
        if err == nil {
            return result, nil
        }
        if !IsTransient(err) || attempt == maxAttempts-1 {
            return zero, fmt.Errorf("after %d attempts: %w", attempt+1, err)
        }
        base := time.Duration(1<<uint(attempt)) * 500 * time.Millisecond
        jitter := time.Duration(rand.Int64N(int64(base / 2)))
        select {
        case <-ctx.Done():
            return zero, ctx.Err()
        case <-time.After(min(base+jitter, 10*time.Second)):
        }
    }
    return zero, errors.New("unreachable")
}
```

## Circuit Breaker

### Java (Resilience4j)
```java
@Bean
public CircuitBreakerConfig circuitBreakerConfig() {
    return CircuitBreakerConfig.custom()
        .failureRateThreshold(50)
        .slowCallRateThreshold(80)
        .slowCallDurationThreshold(Duration.ofSeconds(2))
        .waitDurationInOpenState(Duration.ofSeconds(30))
        .slidingWindowType(SlidingWindowType.COUNT_BASED)
        .slidingWindowSize(10)
        .minimumNumberOfCalls(5)
        .permittedNumberOfCallsInHalfOpenState(3)
        .build();
}

@CircuitBreaker(name = "paymentGateway", fallbackMethod = "paymentFallback")
public PaymentResult processPayment(PaymentRequest req) {
    return gateway.charge(req);
}
```

### Python (pybreaker)
```python
import pybreaker

payment_breaker = pybreaker.CircuitBreaker(
    fail_max=5,
    reset_timeout=30,
    exclude=[BusinessError],
)

@payment_breaker
async def process_payment(request: PaymentRequest) -> PaymentResult:
    return await gateway.charge(request)
```

### Go (gobreaker)
```go
var paymentBreaker = gobreaker.NewCircuitBreaker(gobreaker.Settings{
    Name:        "payment-gateway",
    MaxRequests: 3,                      // half-open
    Interval:    10 * time.Second,       // closed window
    Timeout:     30 * time.Second,       // open → half-open
    ReadyToTrip: func(counts gobreaker.Counts) bool {
        return counts.ConsecutiveFailures > 5
    },
    OnStateChange: func(name string, from, to gobreaker.State) {
        slog.Warn("circuit breaker state change", "name", name, "from", from, "to", to)
    },
})

func ProcessPayment(ctx context.Context, req PaymentRequest) (PaymentResult, error) {
    result, err := paymentBreaker.Execute(func() (interface{}, error) {
        return gateway.Charge(ctx, req)
    })
    if err != nil {
        return PaymentResult{}, err
    }
    return result.(PaymentResult), nil
}
```

## Bulkhead (isolamento de concorrencia)

### Java (Resilience4j)
```java
@Bulkhead(name = "orderService", type = Bulkhead.Type.SEMAPHORE)
// ou @Bulkhead(name = "orderService", type = Bulkhead.Type.THREADPOOL)
public Order getOrder(String id) { return service.find(id); }
```
```yaml
# application.yml
resilience4j.bulkhead.instances.orderService:
  maxConcurrentCalls: 25
  maxWaitDuration: 500ms
```

### Python (asyncio.Semaphore)
```python
_order_semaphore = asyncio.Semaphore(25)

async def get_order(order_id: str) -> Order:
    async with _order_semaphore:
        return await service.find(order_id)
```

### Go (channel semaphore)
```go
var orderSem = make(chan struct{}, 25)

func GetOrder(ctx context.Context, id string) (Order, error) {
    select {
    case orderSem <- struct{}{}:
        defer func() { <-orderSem }()
        return service.Find(ctx, id)
    case <-ctx.Done():
        return Order{}, ctx.Err()
    }
}
```

## Rate Limiting

### Java (Resilience4j)
```java
@RateLimiter(name = "externalApi")
public ExternalData callExternal(String query) { return client.search(query); }
```
```yaml
resilience4j.ratelimiter.instances.externalApi:
  limitForPeriod: 50
  limitRefreshPeriod: 1s
  timeoutDuration: 500ms
```

### Python (aiolimiter)
```python
from aiolimiter import AsyncLimiter

rate_limiter = AsyncLimiter(max_rate=50, time_period=1)

async def call_external(query: str) -> ExternalData:
    async with rate_limiter:
        return await client.search(query)
```

### Go (rate.Limiter)
```go
var externalLimiter = rate.NewLimiter(rate.Limit(50), 10) // 50/s, burst 10

func CallExternal(ctx context.Context, query string) (ExternalData, error) {
    if err := externalLimiter.Wait(ctx); err != nil {
        return ExternalData{}, fmt.Errorf("rate limited: %w", err)
    }
    return client.Search(ctx, query)
}
```

## Timeout explicito

```java
// Java — RestClient/WebClient
var response = restClient.get().uri("/orders/{id}", id)
    .retrieve().body(Order.class);
// Configurar via application.yml:
// spring.http.client.connect-timeout=2s
// spring.http.client.read-timeout=5s
```

```python
# Python — httpx
async with httpx.AsyncClient(timeout=httpx.Timeout(connect=2.0, read=5.0)) as client:
    response = await client.get(f"/orders/{order_id}")
```

```go
// Go — context deadline
ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
defer cancel()
order, err := client.GetOrder(ctx, id)
```

## Quando usar cada padrao

| Padrao | Quando | Nao usar |
|--------|--------|----------|
| **Retry** | Falhas transientes (timeout, 503, rede) | Erros de negocio (400, 422) |
| **Circuit Breaker** | Dependencia instavel, proteger cascata | Chamada local sem I/O |
| **Bulkhead** | Isolar impacto de dependencia lenta | Tudo tem mesma prioridade |
| **Rate Limiting** | API externa com quota, proteger downstream | Chamadas internas sem custo |
| **Timeout** | **Sempre** — toda chamada I/O | Nunca omitir |

## Composicao (Java — Resilience4j)

Ordem recomendada: Retry → CircuitBreaker → RateLimiter → Bulkhead → Timeout

```yaml
resilience4j:
  retry.instances.orderService:
    maxAttempts: 3
    waitDuration: 500ms
  circuitbreaker.instances.orderService:
    failureRateThreshold: 50
    slidingWindowSize: 10
  bulkhead.instances.orderService:
    maxConcurrentCalls: 25
```

```java
@Retry(name = "orderService")
@CircuitBreaker(name = "orderService")
@Bulkhead(name = "orderService")
public Order getOrder(String id) { return client.fetchOrder(id); }
```
