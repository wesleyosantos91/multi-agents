# Jakarta EE 11 + MicroProfile 7.0 — Patterns & Idioms

Padrões e idiomas para Jakarta EE em produção com servidores de aplicação certificados.

## Filosofia

- **Standards-first**: APIs padronizadas, portáveis entre servidores
- **CDI como backbone**: injeção de dependência, eventos, interceptors, decorators
- **MicroProfile complementa**: config externalizada, fault tolerance, health, metrics, OpenAPI

## Estrutura de projeto

```
src/main/java/<package>/
├── web/
│   └── api/           # JAX-RS resources
├── service/           # EJB ou CDI beans de negócio
├── repository/        # JPA repositories
├── model/             # Entities, DTOs
├── event/             # CDI Events, JMS listeners
├── config/            # MicroProfile Config sources
└── interceptor/       # CDI interceptors
src/main/resources/
├── META-INF/
│   ├── persistence.xml
│   ├── beans.xml
│   └── microprofile-config.properties
└── webapp/WEB-INF/
    └── web.xml (opcional)
```

## CDI (Contexts and Dependency Injection)

```java
// Scopes
@ApplicationScoped  // Singleton na aplicação
@RequestScoped      // Um por request
@SessionScoped      // Um por sessão HTTP
@Dependent          // Novo a cada injection point
@TransactionScoped  // Vive durante a transação JTA

// Producer para tipos que não controlamos
@ApplicationScoped
public class ResourceProducer {

    @Produces
    @ApplicationScoped
    public ObjectMapper objectMapper() {
        return new ObjectMapper()
            .registerModule(new JavaTimeModule())
            .disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
    }
}

// Qualifiers
@Qualifier
@Retention(RUNTIME)
@Target({FIELD, PARAMETER, METHOD, TYPE})
public @interface Cached {}

@Cached @ApplicationScoped
public class CachedOrderRepository implements OrderRepository { }
```

## JAX-RS (REST)

```java
@Path("/api/v1/orders")
@ApplicationScoped
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class OrderResource {

    @Inject OrderService service;

    @GET
    public Response list(
        @QueryParam("status") OrderStatus status,
        @QueryParam("page") @DefaultValue("0") int page,
        @QueryParam("size") @DefaultValue("20") int size
    ) {
        var orders = service.list(status, page, size);
        return Response.ok(orders).build();
    }

    @POST
    public Response create(@Valid CreateOrderRequest request) {
        var order = service.create(request);
        return Response.status(Status.CREATED)
            .entity(order)
            .header("Location", "/api/v1/orders/" + order.id())
            .build();
    }

    @GET @Path("/{id}")
    public Response get(@PathParam("id") String id) {
        return service.findById(id)
            .map(Response::ok)
            .orElse(Response.status(Status.NOT_FOUND))
            .build();
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
            .entity(Map.of(
                "type", ex.getType(),
                "title", "Domain Error",
                "detail", ex.getMessage()
            ))
            .type(MediaType.APPLICATION_JSON)
            .build();
    }
}

@Provider
public class ConstraintViolationMapper implements ExceptionMapper<ConstraintViolationException> {
    @Override
    public Response toResponse(ConstraintViolationException ex) {
        var errors = ex.getConstraintViolations().stream()
            .map(v -> Map.of("field", v.getPropertyPath().toString(), "message", v.getMessage()))
            .toList();
        return Response.status(Status.BAD_REQUEST)
            .entity(Map.of("type", "validation-error", "errors", errors))
            .build();
    }
}
```

## JPA (Persistence)

```java
@Entity
@Table(name = "orders")
public class Order {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private String id;

    @Column(nullable = false)
    @Enumerated(EnumType.STRING)
    private OrderStatus status;

    @Column(nullable = false, updatable = false)
    private Instant createdAt;

    @Version
    private Long version;  // Optimistic locking

    @PrePersist
    void onCreate() {
        this.createdAt = Instant.now();
    }
}

// Repository
@ApplicationScoped
public class OrderRepository {

    @PersistenceContext
    EntityManager em;

    public Optional<Order> findById(String id) {
        return Optional.ofNullable(em.find(Order.class, id));
    }

    public List<Order> findByStatus(OrderStatus status, int page, int size) {
        return em.createQuery("SELECT o FROM Order o WHERE o.status = :status ORDER BY o.createdAt DESC", Order.class)
            .setParameter("status", status)
            .setFirstResult(page * size)
            .setMaxResults(size)
            .getResultList();
    }
}
```

## CDI Events

```java
// Evento de domínio
public record OrderCreatedEvent(String orderId, Instant timestamp) {}

// Produtor
@ApplicationScoped
public class OrderService {

    @Inject Event<OrderCreatedEvent> orderCreated;

    @Transactional
    public Order create(CreateOrderRequest request) {
        var order = new Order(request);
        repository.persist(order);
        orderCreated.fire(new OrderCreatedEvent(order.getId(), Instant.now()));
        return order;
    }
}

// Observer
@ApplicationScoped
public class OrderEventHandler {

    public void onOrderCreated(@Observes OrderCreatedEvent event) {
        // Síncrono, mesma transação
    }

    public void onOrderCreatedAsync(@ObservesAsync OrderCreatedEvent event) {
        // Assíncrono, fora da transação
    }
}
```

## JMS (Messaging)

```java
@ApplicationScoped
public class OrderMessageProducer {

    @Inject JMSContext context;

    @Resource(lookup = "java:/jms/queue/orders")
    Queue ordersQueue;

    public void send(OrderEvent event) {
        context.createProducer()
            .setDeliveryMode(DeliveryMode.PERSISTENT)
            .setProperty("eventType", event.type())
            .send(ordersQueue, Json.createObjectBuilder()
                .add("orderId", event.orderId())
                .add("type", event.type())
                .build()
                .toString());
    }
}

@MessageDriven(activationConfig = {
    @ActivationConfigProperty(propertyName = "destinationType", propertyValue = "jakarta.jms.Queue"),
    @ActivationConfigProperty(propertyName = "destination", propertyValue = "java:/jms/queue/orders")
})
public class OrderMessageConsumer implements MessageListener {

    @Inject OrderService service;

    @Override
    public void onMessage(Message message) {
        try {
            var body = message.getBody(String.class);
            service.process(body);
        } catch (JMSException e) {
            throw new RuntimeException("Failed to process message", e);
        }
    }
}
```

## MicroProfile Config

```java
@ApplicationScoped
public class PaymentConfig {

    @Inject @ConfigProperty(name = "payment.api.url")
    String apiUrl;

    @Inject @ConfigProperty(name = "payment.api.timeout", defaultValue = "5000")
    int timeout;

    @Inject @ConfigProperty(name = "payment.retry.max", defaultValue = "3")
    int maxRetries;
}

// microprofile-config.properties
// payment.api.url=https://payment.example.com
// Overridden by env: PAYMENT_API_URL
```

## MicroProfile Fault Tolerance

```java
@ApplicationScoped
public class PaymentService {

    @Retry(maxRetries = 3, delay = 500, jitter = 200)
    @CircuitBreaker(requestVolumeThreshold = 10, failureRatio = 0.5, delay = 30000)
    @Timeout(5000)
    @Fallback(fallbackMethod = "paymentFallback")
    @Bulkhead(value = 10, waitingTaskQueue = 20)
    public PaymentResult process(PaymentRequest request) {
        return paymentClient.charge(request);
    }

    PaymentResult paymentFallback(PaymentRequest request) {
        return new PaymentPending(UUID.randomUUID().toString());
    }
}
```

## MicroProfile Health

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
public class DatabaseReadiness implements HealthCheck {

    @PersistenceContext EntityManager em;

    @Override
    public HealthCheckResponse call() {
        try {
            em.createNativeQuery("SELECT 1").getSingleResult();
            return HealthCheckResponse.up("database");
        } catch (Exception e) {
            return HealthCheckResponse.down("database");
        }
    }
}
```

## MicroProfile REST Client

```java
@RegisterRestClient(configKey = "payment-api")
@Path("/payments")
public interface PaymentClient {

    @POST
    @Consumes(MediaType.APPLICATION_JSON)
    @Produces(MediaType.APPLICATION_JSON)
    PaymentResult charge(PaymentRequest request);
}

// microprofile-config.properties
// payment-api/mp-rest/url=https://payment.example.com
// payment-api/mp-rest/connectTimeout=5000
// payment-api/mp-rest/readTimeout=10000
```

## Interceptors

```java
@InterceptorBinding
@Retention(RUNTIME)
@Target({METHOD, TYPE})
public @interface Logged {}

@Logged
@Interceptor
@Priority(Interceptor.Priority.APPLICATION)
public class LoggingInterceptor {

    private static final Logger log = Logger.getLogger(LoggingInterceptor.class.getName());

    @AroundInvoke
    public Object logInvocation(InvocationContext ctx) throws Exception {
        var start = System.nanoTime();
        try {
            return ctx.proceed();
        } finally {
            var duration = Duration.ofNanos(System.nanoTime() - start);
            log.info(() -> "%s.%s completed in %dms".formatted(
                ctx.getTarget().getClass().getSimpleName(),
                ctx.getMethod().getName(),
                duration.toMillis()));
        }
    }
}
```

## Servidores de aplicação

| Servidor | Jakarta EE | MicroProfile | Notas |
|----------|-----------|-------------|-------|
| WildFly | 11 | 7.0 | Red Hat, comunidade ativa |
| Open Liberty | 11 | 7.0 | IBM, config por features |
| Payara | 11 | 7.0 | Derivado GlassFish, suporte comercial |
| TomEE | 10 | 6.1 | Apache, leve, baseado em Tomcat |
| GlassFish | 11 | — | RI, não recomendado para produção |

## Checklist

- [ ] CDI scopes corretos (@ApplicationScoped para services)?
- [ ] Exception mappers para erros de domínio e validação?
- [ ] JPA com optimistic locking (@Version)?
- [ ] MicroProfile Fault Tolerance para chamadas externas?
- [ ] MicroProfile Health (liveness + readiness)?
- [ ] MicroProfile Config para externalizar configuração?
- [ ] CDI Events para desacoplamento interno?
- [ ] Interceptors para cross-cutting concerns?
- [ ] beans.xml com bean-discovery-mode="annotated"?
- [ ] persistence.xml com validation-mode=CALLBACK?
