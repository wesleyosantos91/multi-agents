---
name: java-project-setup
description: Skill importada do EXEMPLO (java-project-setup.md).
allowed-tools: "read,search"
user-invocable: true
---

# Skill

---
name: java-project-setup
description: "Estrutura e setup de projetos Java modernos com Spring Boot, Quarkus ou Micronaut. Use quando criar projeto Java, configurar framework, ou revisar estrutura Java."
---

# Java Project Setup — Modern Best Practices

Guia para estruturar e configurar projetos Java modernos (Java 21+).

## Escolha de framework

| Critério | Spring Boot | Quarkus | Micronaut |
|----------|-------------|---------|-----------|
| Ecossistema | Maior, mais maduro | Crescente, Red Hat | Crescente, OCI |
| Startup | Moderado (melhor com virtual threads) | Rápido (build-time) | Rápido (AOT) |
| Memória | Moderado | Baixo | Baixo |
| Lambda | Bom com SnapStart | Excelente nativo | Bom nativo |
| Learning curve | Baixa (muita doc) | Média | Média |
| Ideal para | Maioria dos casos | Serverless, containers | Microservices leves |

## Estrutura de projeto

```
src/main/java/<base-package>/
├── Application.java
├── web/
│   ├── api/             # REST controllers, request/response DTOs, exception handlers
│   ├── grpc/            # gRPC services (se aplicável)
│   └── graphql/         # GraphQL resolvers (se aplicável)
├── message/
│   ├── kafka/           # Kafka consumers/producers
│   └── sqs/             # SQS listeners/senders
├── domain/
│   ├── model/           # Entidades, value objects
│   ├── service/         # Lógica de negócio
│   ├── repository/      # Contratos de persistência
│   ├── event/           # Eventos de domínio
│   └── exception/       # Exceções de domínio
├── infrastructure/
│   ├── persistence/     # Implementação JPA/JDBC, mappers
│   ├── client/          # Clientes HTTP para serviços externos
│   ├── config/          # Configuração do framework
│   └── security/        # Configuração de segurança
└── core/
    ├── annotation/      # Annotations customizadas
    ├── validation/      # Validações compartilhadas
    └── mapper/          # Mappers reutilizáveis
```

## Java moderno — Features essenciais

### Records (DTOs, value objects)
```java
public record OrderRequest(
    @NotBlank String customerId,
    @NotEmpty List<OrderItem> items
) {}

public record OrderResponse(
    String id,
    String status,
    BigDecimal total,
    Instant createdAt
) {}
```

### Sealed interfaces (hierarquias controladas)
```java
public sealed interface PaymentResult
    permits PaymentApproved, PaymentDeclined, PaymentPending {
}

public record PaymentApproved(String transactionId, Instant approvedAt) implements PaymentResult {}
public record PaymentDeclined(String reason) implements PaymentResult {}
public record PaymentPending(String pendingId) implements PaymentResult {}
```

### Pattern matching
```java
return switch (result) {
    case PaymentApproved a -> ResponseEntity.ok(a);
    case PaymentDeclined d -> ResponseEntity.unprocessableEntity().body(d);
    case PaymentPending p  -> ResponseEntity.accepted().body(p);
};
```

### Virtual threads (Spring Boot 3.2+)
```yaml
# application.yml
spring:
  threads:
    virtual:
      enabled: true
```

### Structured concurrency (preview)
```java
try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
    var orderTask = scope.fork(() -> orderService.find(orderId));
    var paymentTask = scope.fork(() -> paymentService.find(orderId));
    scope.join().throwIfFailed();
    return new OrderDetail(orderTask.get(), paymentTask.get());
}
```

## Spring Boot — Configuração essencial

### application.yml
```yaml
spring:
  application:
    name: order-service
  datasource:
    url: jdbc:postgresql://localhost:5432/orders
    hikari:
      maximum-pool-size: 10
      connection-timeout: 5000
  jpa:
    open-in-view: false  # SEMPRE false
    hibernate:
      ddl-auto: validate  # nunca update/create em produção
  jackson:
    default-property-inclusion: non_null
    serialization:
      write-dates-as-timestamps: false

management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  endpoint:
    health:
      show-details: when_authorized
      probes:
        enabled: true  # readiness + liveness

server:
  shutdown: graceful
  tomcat:
    connection-timeout: 5s
```

### Exception handling global
```java
@RestControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ConstraintViolationException.class)
    ProblemDetail handleValidation(ConstraintViolationException ex) {
        var problem = ProblemDetail.forStatusAndDetail(
            HttpStatus.BAD_REQUEST, "Validation failed");
        problem.setProperty("violations", ex.getConstraintViolations().stream()
            .map(v -> Map.of("field", v.getPropertyPath().toString(), "message", v.getMessage()))
            .toList());
        return problem;
    }

    @ExceptionHandler(EntityNotFoundException.class)
    ProblemDetail handleNotFound(EntityNotFoundException ex) {
        return ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, ex.getMessage());
    }
}
```

## Testes

### Stack de testes recomendada
```xml
<!-- JUnit 5 (vem com Spring Boot) -->
<!-- AssertJ para assertions fluentes -->
<dependency>
    <groupId>org.assertj</groupId>
    <artifactId>assertj-core</artifactId>
    <scope>test</scope>
</dependency>
<!-- Testcontainers para integração -->
<dependency>
    <groupId>org.testcontainers</groupId>
    <artifactId>junit-jupiter</artifactId>
    <scope>test</scope>
</dependency>
<!-- ArchUnit para testes de arquitetura -->
<dependency>
    <groupId>com.tngtech.archunit</groupId>
    <artifactId>archunit-junit5</artifactId>
    <scope>test</scope>
</dependency>
```

### Teste de arquitetura (ArchUnit)
```java
@AnalyzeClasses(packages = "com.example")
class ArchitectureTest {

    @ArchTest
    static final ArchRule domainShouldNotDependOnInfrastructure =
        noClasses().that().resideInAPackage("..domain..")
            .should().dependOnClassesThat().resideInAPackage("..infrastructure..");

    @ArchTest
    static final ArchRule controllersShouldNotAccessRepositories =
        noClasses().that().resideInAPackage("..web..")
            .should().dependOnClassesThat().resideInAPackage("..repository..");
}
```

## Checklist
- [ ] Java 21+ como baseline?
- [ ] Records para DTOs e value objects?
- [ ] `spring.jpa.open-in-view: false`?
- [ ] Graceful shutdown configurado?
- [ ] Health probes (readiness/liveness) habilitados?
- [ ] Exception handler global com ProblemDetail?
- [ ] Testes com Testcontainers para integração?
- [ ] ArchUnit validando boundaries?
- [ ] Virtual threads habilitados (quando Spring Boot 3.2+)?
