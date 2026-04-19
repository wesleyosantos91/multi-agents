---
name: graphql-patterns
description: "Padrões GraphQL: schema design, resolvers, N+1 (DataLoader), pagination, subscriptions, testing. Use quando implementar ou revisar APIs GraphQL."
---

# GraphQL — Patterns & Idioms

Padroes e idiomas para GraphQL em producao.

## Quando usar GraphQL vs REST

| Criterio | GraphQL | REST |
|----------|---------|------|
| Multiplos consumers com necessidades diferentes | Preferido | Over/under-fetching |
| Frontend precisa compor dados de varias fontes | Preferido | Multiplas chamadas |
| CRUD simples com 1 consumer | Overhead | Preferido |
| Caching (HTTP-level) | Complexo | Simples |
| Real-time | Subscriptions | WebSocket/SSE |
| Upload de arquivos | Complexo | Simples |

## Schema design

```graphql
type Query {
  order(id: ID!): Order
  orders(filter: OrderFilter, pagination: PaginationInput): OrderConnection!
}

type Mutation {
  createOrder(input: CreateOrderInput!): CreateOrderPayload!
  updateOrder(id: ID!, input: UpdateOrderInput!): UpdateOrderPayload!
  cancelOrder(id: ID!): CancelOrderPayload!
}

type Subscription {
  orderStatusChanged(orderId: ID!): OrderStatusEvent!
}

# Entities
type Order implements Node {
  id: ID!
  title: String!
  amount: Float!
  status: OrderStatus!
  customer: Customer!
  items: [OrderItem!]!
  createdAt: DateTime!
  updatedAt: DateTime!
}

type Customer {
  id: ID!
  name: String!
  email: String!
  orders(first: Int, after: String): OrderConnection!
}

type OrderItem {
  id: ID!
  product: Product!
  quantity: Int!
  unitPrice: Float!
}

# Enums
enum OrderStatus {
  PENDING
  CONFIRMED
  SHIPPED
  DELIVERED
  CANCELLED
}

# Input types
input CreateOrderInput {
  title: String!
  items: [OrderItemInput!]!
}

input OrderItemInput {
  productId: ID!
  quantity: Int!
}

input OrderFilter {
  status: OrderStatus
  customerId: ID
  dateRange: DateRangeInput
}

input PaginationInput {
  first: Int
  after: String
  last: Int
  before: String
}

# Mutation payloads (sempre wrapper, nunca entity direto)
type CreateOrderPayload {
  order: Order
  errors: [UserError!]!
}

type UserError {
  field: String
  message: String!
  code: ErrorCode!
}

enum ErrorCode {
  VALIDATION_ERROR
  NOT_FOUND
  CONFLICT
  UNAUTHORIZED
}

# Relay-style pagination
type OrderConnection {
  edges: [OrderEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type OrderEdge {
  node: Order!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

# Interfaces
interface Node {
  id: ID!
}

# Scalars
scalar DateTime
scalar JSON
```

## Resolvers (Java — Spring for GraphQL)

```java
@Controller
public class OrderController {

    private final OrderService orderService;

    @QueryMapping
    public Order order(@Argument String id) {
        return orderService.findById(id)
            .orElseThrow(() -> new GraphQLException("Order not found"));
    }

    @QueryMapping
    public OrderConnection orders(@Argument OrderFilter filter, @Argument PaginationInput pagination) {
        return orderService.list(filter, pagination);
    }

    @MutationMapping
    public CreateOrderPayload createOrder(@Argument CreateOrderInput input) {
        try {
            var order = orderService.create(input);
            return new CreateOrderPayload(order, List.of());
        } catch (ValidationException e) {
            return new CreateOrderPayload(null, e.toUserErrors());
        }
    }

    // Nested resolver — resolve customer para cada order
    @SchemaMapping(typeName = "Order", field = "customer")
    public Customer customer(Order order) {
        return customerService.findById(order.getCustomerId());
    }
}
```

## N+1 — DataLoader

O problema mais critico em GraphQL. Sem DataLoader, buscar 20 orders com customer faz 1 + 20 queries.

```java
// Java — Spring for GraphQL BatchMapping
@Controller
public class OrderController {

    // BatchMapping resolve N+1 automaticamente
    @BatchMapping(typeName = "Order", field = "customer")
    public Map<Order, Customer> customers(List<Order> orders) {
        var customerIds = orders.stream().map(Order::getCustomerId).distinct().toList();
        var customersMap = customerService.findByIds(customerIds).stream()
            .collect(Collectors.toMap(Customer::getId, Function.identity()));
        return orders.stream()
            .collect(Collectors.toMap(Function.identity(), o -> customersMap.get(o.getCustomerId())));
    }
}
```

```javascript
// Node.js — DataLoader
const customerLoader = new DataLoader(async (customerIds) => {
  const customers = await customerService.findByIds(customerIds);
  const map = new Map(customers.map(c => [c.id, c]));
  return customerIds.map(id => map.get(id));
});

const resolvers = {
  Order: {
    customer: (order, _, { loaders }) => loaders.customerLoader.load(order.customerId),
  },
};
```

```python
# Python — Strawberry + DataLoader
from strawberry.dataloader import DataLoader

async def load_customers(keys: list[str]) -> list[Customer]:
    customers = await customer_service.find_by_ids(keys)
    customer_map = {c.id: c for c in customers}
    return [customer_map[key] for key in keys]

customer_loader = DataLoader(load_fn=load_customers)

@strawberry.type
class Order:
    id: str
    customer_id: str

    @strawberry.field
    async def customer(self, info) -> Customer:
        return await info.context.customer_loader.load(self.customer_id)
```

## Query complexity e depth limiting

```java
// Spring for GraphQL — limitar profundidade e complexidade
@Configuration
public class GraphQLConfig {
    @Bean
    public RuntimeWiringConfigurer runtimeWiringConfigurer() {
        return builder -> builder
            .directive("complexity", new ComplexityDirective())
            .build();
    }
}

// schema
directive @complexity(value: Int!) on FIELD_DEFINITION

type Customer {
  orders(first: Int, after: String): OrderConnection! @complexity(value: 10)
}
```

```yaml
# application.yml
spring:
  graphql:
    schema:
      inspection:
        enabled: true
    # Limitar depth — evitar queries recursivas
    # Implementar via instrumentação customizada
```

## Pagination (Relay cursor-based)

```java
public OrderConnection list(OrderFilter filter, PaginationInput pagination) {
    int limit = Math.min(pagination.first() != null ? pagination.first() : 20, 100);
    String afterCursor = pagination.after();

    var orders = repository.findWithCursor(filter, afterCursor, limit + 1);
    boolean hasNextPage = orders.size() > limit;
    if (hasNextPage) orders = orders.subList(0, limit);

    var edges = orders.stream()
        .map(o -> new OrderEdge(o, encodeCursor(o.getId())))
        .toList();

    return new OrderConnection(
        edges,
        new PageInfo(hasNextPage, false,
            edges.isEmpty() ? null : edges.getFirst().cursor(),
            edges.isEmpty() ? null : edges.getLast().cursor()),
        repository.count(filter)
    );
}

private String encodeCursor(String id) {
    return Base64.getEncoder().encodeToString(id.getBytes());
}
```

## Error handling

```graphql
# Mutation sempre retorna payload com errors (nao throw)
type CreateOrderPayload {
  order: Order           # null se erro
  errors: [UserError!]!  # vazio se sucesso
}
```

```java
// Erros de negocio → no payload (nao exception)
@MutationMapping
public CreateOrderPayload createOrder(@Argument CreateOrderInput input) {
    var errors = validator.validate(input);
    if (!errors.isEmpty()) {
        return new CreateOrderPayload(null, errors);
    }
    var order = orderService.create(input);
    return new CreateOrderPayload(order, List.of());
}

// Erros de sistema → GraphQL errors (exception)
// Nao expor detalhes internos ao client
@QueryMapping
public Order order(@Argument String id) {
    return orderService.findById(id)
        .orElseThrow(() -> new GraphQLException("Order not found"));
}
```

## Testing

```java
@SpringBootTest
@AutoConfigureHttpGraphQlTester
class OrderControllerTest {

    @Autowired
    private HttpGraphQlTester tester;

    @Test
    void shouldGetOrder() {
        tester.document("""
            query {
              order(id: "1") {
                id
                title
                status
              }
            }
            """)
            .execute()
            .path("order.id").entity(String.class).isEqualTo("1")
            .path("order.title").entity(String.class).isEqualTo("Test Order")
            .path("order.status").entity(String.class).isEqualTo("PENDING");
    }

    @Test
    void shouldCreateOrder() {
        tester.document("""
            mutation($input: CreateOrderInput!) {
              createOrder(input: $input) {
                order { id title }
                errors { message code }
              }
            }
            """)
            .variable("input", Map.of("title", "New Order", "items", List.of()))
            .execute()
            .path("createOrder.order.title").entity(String.class).isEqualTo("New Order")
            .path("createOrder.errors").entityList(Object.class).hasSize(0);
    }
}
```

## Checklist

- [ ] Schema-first design (nao code-first)?
- [ ] Mutation payloads com `errors` field (nao throw para erros de negocio)?
- [ ] DataLoader / @BatchMapping para resolver N+1?
- [ ] Cursor-based pagination (Relay spec)?
- [ ] Query depth limiting?
- [ ] Query complexity limiting?
- [ ] Enum com valor UNSPECIFIED ou tratamento de null?
- [ ] Input validation antes de processar?
- [ ] Testes de integracao com GraphQlTester?
- [ ] Subscriptions com auth e cleanup?
