# Spring Boot — Patterns & Idioms

Padrões e idiomas para Spring Boot em produção.

## Bean Lifecycle & Configuration

### Configuration properties (type-safe)
```java
@ConfigurationProperties(prefix = "app.payment")
public record PaymentProperties(
    String apiUrl,
    Duration timeout,
    int maxRetries
) {}

// Ativar
@EnableConfigurationProperties(PaymentProperties.class)
```

### Conditional beans
```java
@Bean
@ConditionalOnProperty(name = "app.cache.enabled", havingValue = "true")
CacheManager cacheManager() { ... }

@Bean
@Profile("!test")
SqsClient sqsClient() { ... }
```

## Resilience (Spring + Resilience4j)

### Circuit Breaker
```java
@CircuitBreaker(name = "paymentService", fallbackMethod = "paymentFallback")
public PaymentResult processPayment(PaymentRequest request) {
    return paymentClient.charge(request);
}

private PaymentResult paymentFallback(PaymentRequest request, Exception ex) {
    log.warn("Payment circuit open, queuing for retry: {}", ex.getMessage());
    return new PaymentPending(UUID.randomUUID().toString());
}
```

### Retry + Rate Limiter
```yaml
resilience4j:
  circuitbreaker:
    instances:
      paymentService:
        sliding-window-size: 10
        failure-rate-threshold: 50
        wait-duration-in-open-state: 30s
  retry:
    instances:
      paymentService:
        max-attempts: 3
        wait-duration: 500ms
        exponential-backoff-multiplier: 2
  ratelimiter:
    instances:
      paymentService:
        limit-for-period: 100
        limit-refresh-period: 1s
```

## Security (Spring Security)

### JWT Configuration
```java
@Bean
SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
    return http
        .csrf(AbstractHttpConfigurer::disable)
        .sessionManagement(s -> s.sessionCreationPolicy(STATELESS))
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/actuator/health/**").permitAll()
            .requestMatchers("/api/v1/public/**").permitAll()
            .requestMatchers("/api/v1/admin/**").hasRole("ADMIN")
            .anyRequest().authenticated()
        )
        .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()))
        .build();
}
```

## Messaging

### Kafka Consumer (Spring Kafka)
```java
@KafkaListener(topics = "${app.kafka.topics.orders}", groupId = "${spring.application.name}")
public void consume(@Payload OrderEvent event, @Header(KafkaHeaders.RECEIVED_KEY) String key) {
    log.info("Processing order event: key={}, orderId={}", key, event.orderId());
    orderService.process(event);
}
```

### SQS Consumer (Spring Cloud AWS)
```java
@SqsListener("${app.sqs.queues.orders}")
public void consume(@Payload OrderEvent event, @Headers Map<String, String> headers) {
    log.info("Processing SQS message: orderId={}", event.orderId());
    orderService.process(event);
}
```

## Caching
```java
@Cacheable(value = "products", key = "#productId", unless = "#result == null")
public Product findProduct(String productId) {
    return productRepository.findById(productId).orElse(null);
}

@CacheEvict(value = "products", key = "#product.id")
public Product updateProduct(Product product) {
    return productRepository.save(product);
}
```

## Scheduling
```java
@Scheduled(fixedDelayString = "${app.cleanup.interval:PT1H}")
@SchedulerLock(name = "cleanupExpiredOrders", lockAtLeastFor = "PT5M")
public void cleanupExpiredOrders() {
    int deleted = orderRepository.deleteExpiredBefore(Instant.now().minus(Duration.ofDays(30)));
    log.info("Cleaned up {} expired orders", deleted);
}
```

## Observability (Micrometer + OpenTelemetry)
```java
@Bean
MeterBinder orderMetrics(OrderRepository repository) {
    return registry -> Gauge.builder("orders.pending.count", repository::countPending)
        .description("Number of pending orders")
        .register(registry);
}

// Custom timer
private final Timer orderProcessingTimer;

public void processOrder(Order order) {
    orderProcessingTimer.record(() -> {
        // processing logic
    });
}
```

## Pagination & Filtering
```java
@GetMapping("/orders")
Page<OrderResponse> listOrders(
    @RequestParam(defaultValue = "0") int page,
    @RequestParam(defaultValue = "20") int size,
    @RequestParam(required = false) OrderStatus status,
    @RequestParam(defaultValue = "createdAt,desc") String[] sort
) {
    var pageable = PageRequest.of(page, size, Sort.by(parseSortOrders(sort)));
    var spec = OrderSpecification.builder()
        .status(status)
        .build();
    return orderRepository.findAll(spec, pageable)
        .map(orderMapper::toResponse);
}
```

## Anti-patterns a evitar
- `@Autowired` em campo — preferir constructor injection
- `@Transactional` em classe inteira — ser explícito por método
- Service chamando controller — violação de camadas
- `spring.jpa.open-in-view: true` — N+1 silencioso
- Catch genérico em `@Service` — deixar propagar para o handler global
- `@Async` sem executor configurado — usa pool default (perigoso)
