---
name: java-micronaut-patterns
description: "Padrões Micronaut: DI compile-time, HTTP client/server, GraalVM native, Lambda e data access. Use quando implementar features em Micronaut ou configurar projeto Micronaut."
---

# Micronaut — Patterns & Idioms

Padrões e idiomas para Micronaut em produção.

## Filosofia Micronaut
- **Compile-time DI**: sem reflection em runtime → startup rápido, baixo footprint
- **AOT processing**: configuração, validação e DI resolvidos em build
- **Cloud-native**: suporte nativo a Lambda, GraalVM, service discovery

## Estrutura de projeto
```
src/main/java/<package>/
├── controller/        # HTTP endpoints
├── service/           # Lógica de negócio
├── repository/        # Persistência (Micronaut Data)
├── model/             # Entidades, DTOs
├── client/            # HTTP clients declarativos
└── config/            # Configuração customizada
src/main/resources/
└── application.yml    # Configuração principal
```

## DI (Compile-time)
```java
// Scopes
@Singleton       // Um por aplicação (padrão para services)
@RequestScope    // Um por request HTTP
@Prototype       // Novo a cada injection

@Singleton
public class OrderService {
    private final OrderRepository repository;
    private final PaymentClient paymentClient;

    // Constructor injection (preferido em Micronaut)
    public OrderService(OrderRepository repository, PaymentClient paymentClient) {
        this.repository = repository;
        this.paymentClient = paymentClient;
    }
}
```

## HTTP Controller
```java
@Controller("/api/v1/orders")
public class OrderController {

    private final OrderService service;

    public OrderController(OrderService service) {
        this.service = service;
    }

    @Get("{?status,page,size}")
    public List<OrderResponse> list(
        @Nullable OrderStatus status,
        @QueryValue(defaultValue = "0") int page,
        @QueryValue(defaultValue = "20") int size
    ) {
        return service.list(status, page, size);
    }

    @Post
    @Status(HttpStatus.CREATED)
    public OrderResponse create(@Body @Valid CreateOrderRequest request) {
        return service.create(request);
    }

    @Get("/{id}")
    public OrderResponse get(String id) {
        return service.findById(id)
            .orElseThrow(() -> new HttpStatusException(HttpStatus.NOT_FOUND, "Order not found"));
    }
}
```

## Error Handler
```java
@Singleton
@Produces
@Requires(classes = DomainException.class)
public class DomainExceptionHandler implements ExceptionHandler<DomainException, HttpResponse<?>> {

    @Override
    public HttpResponse<?> handle(HttpRequest request, DomainException ex) {
        return HttpResponse.unprocessableEntity()
            .body(Map.of("type", ex.getType(), "detail", ex.getMessage()));
    }
}
```

## Declarative HTTP Client
```java
@Client("payment-api")
public interface PaymentClient {

    @Post("/payments")
    PaymentResult charge(@Body PaymentRequest request);
}

// application.yml
micronaut:
  http:
    client:
      payment-api:
        url: https://payment.example.com
        connect-timeout: 5s
        read-timeout: 10s
```

## Micronaut Data (Repository)
```java
@JdbcRepository(dialect = Dialect.POSTGRES)
public interface OrderRepository extends PageableRepository<Order, String> {

    List<Order> findByStatus(OrderStatus status, Pageable pageable);

    Optional<Order> findById(String id);

    @Query("SELECT o FROM Order o WHERE o.createdAt < :before AND o.status = 'EXPIRED'")
    List<Order> findExpired(Instant before);
}
```

## Resilience (Micronaut Retry)
```java
@Singleton
@Retryable(attempts = "3", delay = "500ms", multiplier = "2")
public class PaymentService {

    @CircuitBreaker(reset = "30s")
    public PaymentResult process(PaymentRequest request) {
        return paymentClient.charge(request);
    }
}
```

## Configuration
```yaml
# application.yml
micronaut:
  application:
    name: order-service
  server:
    port: 8080

datasources:
  default:
    url: jdbc:postgresql://localhost:5432/orders
    driver-class-name: org.postgresql.Driver

# Environment-specific
---
micronaut:
  environments: dev
datasources:
  default:
    url: jdbc:postgresql://localhost:5432/orders_dev
```

## Health Indicators
```java
@Singleton
@Liveness
public class LivenessIndicator implements HealthIndicator {
    @Override
    public Publisher<HealthResult> getResult() {
        return Mono.just(HealthResult.builder("alive").status(HealthStatus.UP).build());
    }
}
```

## Lambda Function
```java
@Introspected
public class OrderLambdaHandler extends MicronautRequestHandler<SQSEvent, SQSBatchResponse> {

    @Inject OrderService service;

    @Override
    public SQSBatchResponse execute(SQSEvent event) {
        // handler fino
    }
}
```

## GraalVM Native
```bash
# Build nativo
./gradlew nativeCompile

# Docker nativo
./gradlew dockerBuildNative
```

## Checklist
- [ ] Constructor injection (não field injection)?
- [ ] Scopes corretos (@Singleton para services)?
- [ ] Error handler para exceções de domínio?
- [ ] HTTP clients declarativos com timeout?
- [ ] Retry/CircuitBreaker para chamadas externas?
- [ ] Health indicators (liveness + readiness)?
- [ ] Micronaut Data para persistência (quando JPA/JDBC)?
- [ ] Environment-specific config?
