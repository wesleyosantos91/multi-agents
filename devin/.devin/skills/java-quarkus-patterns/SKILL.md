---
name: java-quarkus-patterns
description: "Padrões Quarkus: CDI, RESTEasy, dev mode, native build, Lambda e extensões. Use quando implementar features em Quarkus ou configurar projeto Quarkus."
argument-hint: "[contexto adicional]"
---

# Quarkus — Patterns & Idioms

Padrões e idiomas para Quarkus em produção.

## Filosofia Quarkus
- **Build-time over runtime**: maior processamento em build → startup mais rápido
- **Standards-based**: CDI, JAX-RS, JPA, MicroProfile — não APIs proprietárias
- **Dev mode**: `quarkus dev` com hot reload e Dev UI

## Estrutura de projeto
```
src/main/java/<package>/
├── resource/          # JAX-RS endpoints (equivalente a controller)
├── service/           # Lógica de negócio
├── repository/        # Persistência (Panache ou plain JPA)
├── model/             # Entidades, DTOs
├── client/            # REST clients (MicroProfile REST Client)
└── config/            # Configuração customizada
src/main/resources/
├── application.properties   # Configuração principal
└── META-INF/resources/      # Static files
```

## CDI (Contexts and Dependency Injection)
```java
// Bean scopes
@ApplicationScoped  // Singleton na aplicação (padrão para services)
@RequestScoped      // Um por request HTTP
@Dependent          // Novo a cada injection point

// Injection
@ApplicationScoped
public class OrderService {
    @Inject OrderRepository repository;  // field injection (OK em Quarkus)
    @Inject @RestClient PaymentClient paymentClient;  // REST Client
}
```

## RESTEasy Reactive (JAX-RS)
```java
@Path("/api/v1/orders")
@ApplicationScoped
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class OrderResource {

    @Inject OrderService service;

    @GET
    public List<OrderResponse> list(
        @QueryParam("status") OrderStatus status,
        @QueryParam("page") @DefaultValue("0") int page,
        @QueryParam("size") @DefaultValue("20") int size
    ) {
        return service.list(status, page, size);
    }

    @POST
    @Transactional
    public Response create(@Valid CreateOrderRequest request) {
        var order = service.create(request);
        return Response.status(Status.CREATED).entity(order).build();
    }

    @GET @Path("/{id}")
    public OrderResponse get(@PathParam("id") String id) {
        return service.findById(id)
            .orElseThrow(() -> new NotFoundException("Order not found: " + id));
    }
}
```

## Exception Mapper
```java
@Provider
public class DomainExceptionMapper implements ExceptionMapper<DomainException> {
    @Override
    public Response toResponse(DomainException ex) {
        return Response.status(422)
            .entity(Map.of("type", ex.getType(), "detail", ex.getMessage()))
            .build();
    }
}
```

## Panache (Repository pattern)
```java
@ApplicationScoped
public class OrderRepository implements PanacheRepositoryBase<Order, String> {

    public List<Order> findByStatus(OrderStatus status, int page, int size) {
        return find("status", Sort.by("createdAt").descending(), status)
            .page(Page.of(page, size))
            .list();
    }
}
```

## MicroProfile REST Client
```java
@RegisterRestClient(configKey = "payment-api")
@Path("/payments")
public interface PaymentClient {

    @POST
    @ClientHeaderParam(name = "X-Request-Id", value = "{generateRequestId}")
    PaymentResult charge(PaymentRequest request);

    default String generateRequestId() {
        return UUID.randomUUID().toString();
    }
}

// application.properties
quarkus.rest-client.payment-api.url=https://payment.example.com
quarkus.rest-client.payment-api.connect-timeout=5000
quarkus.rest-client.payment-api.read-timeout=10000
```

## MicroProfile Fault Tolerance
```java
@ApplicationScoped
public class PaymentService {

    @Inject @RestClient PaymentClient client;

    @Retry(maxRetries = 3, delay = 500)
    @CircuitBreaker(requestVolumeThreshold = 10, failureRatio = 0.5, delay = 30000)
    @Timeout(5000)
    @Fallback(fallbackMethod = "paymentFallback")
    public PaymentResult process(PaymentRequest request) {
        return client.charge(request);
    }

    PaymentResult paymentFallback(PaymentRequest request) {
        return new PaymentPending(UUID.randomUUID().toString());
    }
}
```

## Configuration
```properties
# application.properties
quarkus.http.port=8080
quarkus.datasource.db-kind=postgresql
quarkus.datasource.jdbc.url=jdbc:postgresql://localhost:5432/orders
quarkus.hibernate-orm.database.generation=validate
quarkus.log.console.json=true

# Profiles: dev, test, prod
%dev.quarkus.datasource.jdbc.url=jdbc:postgresql://localhost:5432/orders_dev
%dev.quarkus.log.console.json=false
%dev.quarkus.hibernate-orm.database.generation=drop-and-create
%test.quarkus.datasource.db-kind=h2
```

## Health checks (MicroProfile Health)
```java
@Liveness
@ApplicationScoped
public class LivenessCheck implements HealthCheck {
    @Override
    public HealthCheckResponse call() {
        return HealthCheckResponse.up("alive");
    }
}

@Readiness
@ApplicationScoped
public class DatabaseReadinessCheck implements HealthCheck {
    @Inject DataSource dataSource;

    @Override
    public HealthCheckResponse call() {
        try (var conn = dataSource.getConnection()) {
            return HealthCheckResponse.up("database");
        } catch (Exception e) {
            return HealthCheckResponse.down("database");
        }
    }
}
```

## Lambda deployment
```properties
quarkus.lambda.handler=order-handler
quarkus.package.type=uber-jar  # ou native para GraalVM
```

```java
@Named("order-handler")
@ApplicationScoped
public class OrderLambdaHandler implements RequestHandler<SQSEvent, SQSBatchResponse> {
    @Inject OrderService service;

    @Override
    public SQSBatchResponse handleRequest(SQSEvent event, Context context) {
        // handler fino — delega para service
    }
}
```

## Dev mode
```bash
# Hot reload + Dev UI (localhost:8080/q/dev)
quarkus dev

# Continuous testing (roda testes automaticamente ao salvar)
# Ativado por padrão no dev mode — tecla 'r' para forçar
```

## Checklist
- [ ] RESTEasy Reactive (não classic)?
- [ ] CDI scopes corretos (@ApplicationScoped para services)?
- [ ] Exception mapper para erros de domínio?
- [ ] MicroProfile Fault Tolerance para chamadas externas?
- [ ] Health checks (liveness + readiness)?
- [ ] Profiles configurados (dev, test, prod)?
- [ ] Logs JSON em produção (`quarkus.log.console.json=true`)?
- [ ] Panache para persistência (quando JPA)?
