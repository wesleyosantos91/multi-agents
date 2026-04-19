---
name: java-testing
description: Skill importada do EXEMPLO (java-testing.md).
allowed-tools: "read,search"
user-invocable: true
---

# Skill

---
name: java-testing
description: "Testes Java com JUnit 5, Testcontainers, ArchUnit, PIT e MockMvc. Use quando criar testes Java, configurar Testcontainers, ou melhorar cobertura em projetos Java."
---

# Java Testing — JUnit 5 + Ecosystem

Guia completo de testes para projetos Java.

## Stack de testes

| Ferramenta | Propósito |
|-----------|----------|
| JUnit 5 | Base de testes |
| AssertJ | Assertions fluentes e legíveis |
| Mockito | Mocks e stubs |
| Testcontainers | Banco, broker, AWS real em teste |
| ArchUnit | Testes de arquitetura |
| PIT | Testes de mutação |
| MockMvc / WebTestClient | Testes de API HTTP |
| WireMock | Mock de serviços externos |

## Testes unitários

### Padrão Given-When-Then
```java
@Test
void shouldCalculateOrderTotalWithDiscount() {
    // given
    var items = List.of(
        new OrderItem("prod-1", 2, new BigDecimal("50.00")),
        new OrderItem("prod-2", 1, new BigDecimal("30.00"))
    );
    var discount = new PercentageDiscount(10);

    // when
    var total = Order.calculateTotal(items, discount);

    // then
    assertThat(total).isEqualByComparingTo("117.00"); // (100 + 30) * 0.9
}
```

### Parametrized tests
```java
@ParameterizedTest
@CsvSource({
    "PENDING,   true",
    "CONFIRMED, true",
    "SHIPPED,   false",
    "DELIVERED, false",
    "CANCELLED, false"
})
void shouldIdentifyCancellableStatuses(OrderStatus status, boolean expected) {
    assertThat(status.isCancellable()).isEqualTo(expected);
}
```

### Nested tests
```java
@Nested
class WhenOrderIsPending {
    private Order order;

    @BeforeEach
    void setUp() {
        order = OrderFixture.pendingOrder();
    }

    @Test
    void shouldAllowCancellation() {
        assertThatNoException().isThrownBy(() -> order.cancel());
    }

    @Test
    void shouldAllowConfirmation() {
        order.confirm();
        assertThat(order.getStatus()).isEqualTo(CONFIRMED);
    }
}

@Nested
class WhenOrderIsShipped {
    @Test
    void shouldRejectCancellation() {
        var order = OrderFixture.shippedOrder();
        assertThatThrownBy(() -> order.cancel())
            .isInstanceOf(OrderNotCancellableException.class);
    }
}
```

## Testes de integração (Testcontainers)

### Configuração base
```java
@SpringBootTest
@Testcontainers
class OrderRepositoryIntegrationTest {

    @Container
    static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16-alpine")
        .withDatabaseName("test")
        .withUsername("test")
        .withPassword("test");

    @DynamicPropertySource
    static void configureProperties(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }

    @Autowired
    private OrderRepository repository;

    @Test
    void shouldPersistAndRetrieveOrder() {
        var order = OrderFixture.validOrder();
        var saved = repository.save(order);

        var found = repository.findById(saved.getId());
        assertThat(found).isPresent()
            .get().satisfies(o -> {
                assertThat(o.getCustomerId()).isEqualTo(order.getCustomerId());
                assertThat(o.getStatus()).isEqualTo(PENDING);
            });
    }
}
```

### Testcontainers com Floci (AWS)
```java
@Container
static GenericContainer<?> floci = new GenericContainer<>(
    DockerImageName.parse("ghcr.io/floci/floci:latest"))
    .withExposedPorts(4566)
    .waitingFor(Wait.forHttp("/_floci/health").forPort(4566));

@DynamicPropertySource
static void configureAWS(DynamicPropertyRegistry registry) {
    var endpoint = "http://%s:%d".formatted(floci.getHost(), floci.getMappedPort(4566));
    registry.add("spring.cloud.aws.endpoint", () -> endpoint);
    registry.add("spring.cloud.aws.region.static", () -> "us-east-1");
}
```

## Testes de API (MockMvc)

```java
@WebMvcTest(OrderController.class)
class OrderControllerTest {

    @Autowired MockMvc mockMvc;
    @MockitoBean OrderService orderService;

    @Test
    void shouldCreateOrder() throws Exception {
        var request = """
            {"customerId": "cust-1", "items": [{"productId": "prod-1", "quantity": 2}]}
            """;

        when(orderService.create(any())).thenReturn(OrderFixture.createdOrder());

        mockMvc.perform(post("/api/v1/orders")
                .contentType(APPLICATION_JSON)
                .content(request))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.id").isNotEmpty())
            .andExpect(jsonPath("$.status").value("PENDING"));
    }

    @Test
    void shouldReturn400WhenCustomerIdMissing() throws Exception {
        mockMvc.perform(post("/api/v1/orders")
                .contentType(APPLICATION_JSON)
                .content("""
                    {"items": [{"productId": "prod-1", "quantity": 2}]}
                    """))
            .andExpect(status().isBadRequest());
    }
}
```

## Testes de arquitetura (ArchUnit)

```java
@AnalyzeClasses(packages = "com.example.order")
class ArchitectureTest {

    @ArchTest
    static final ArchRule domainIsIndependent =
        noClasses().that().resideInAPackage("..domain..")
            .should().dependOnClassesThat()
            .resideInAnyPackage("..web..", "..infrastructure..", "..message..");

    @ArchTest
    static final ArchRule servicesShouldNotReturnEntities =
        methods().that().areDeclaredInClassesThat().resideInAPackage("..web.api..")
            .should().haveRawReturnType(resideInAPackage("..web.api.."))
            .orShould().haveRawReturnType(assignableTo(ResponseEntity.class));

    @ArchTest
    static final ArchRule noFieldInjection =
        noFields().should().beAnnotatedWith(Autowired.class);
}
```

## Testes de mutação (PIT)

```xml
<plugin>
    <groupId>org.pitest</groupId>
    <artifactId>pitest-maven</artifactId>
    <configuration>
        <targetClasses>
            <param>com.example.order.domain.*</param>
        </targetClasses>
        <mutationThreshold>80</mutationThreshold>
        <coverageThreshold>85</coverageThreshold>
    </configuration>
</plugin>
```

```bash
mvn pitest:mutationCoverage
```

## Fixtures Pattern
```java
public class OrderFixture {
    public static Order pendingOrder() {
        return Order.builder()
            .id("ord-123")
            .customerId("cust-456")
            .status(PENDING)
            .items(List.of(defaultItem()))
            .build();
    }

    public static OrderItem defaultItem() {
        return new OrderItem("prod-1", 1, new BigDecimal("50.00"));
    }
}
```

## Checklist
- [ ] Testes unitários cobrem lógica de negócio?
- [ ] Testes de integração com Testcontainers (banco real)?
- [ ] Testes de API (MockMvc) para controllers?
- [ ] ArchUnit validando boundaries?
- [ ] PIT rodando em código crítico (domain)?
- [ ] Fixtures reutilizáveis para setup?
- [ ] Sem `@SpringBootTest` em testes unitários (lento)?
- [ ] `-race` equivalent: concurrent tests quando aplicável?
