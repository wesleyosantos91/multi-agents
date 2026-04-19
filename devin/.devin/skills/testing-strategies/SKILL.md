---
name: testing-strategies
description: "Guia de estratégias de teste por tipo e linguagem. Use quando pedirem para criar testes, melhorar cobertura, ou definir estratégia de testes."
argument-hint: "[contexto adicional]"
---

# Testing Strategies

Guia de estratégias de teste para diferentes cenários e linguagens.

## Pirâmide de testes

```
        /  E2E  \          Poucos, lentos, caros — fluxos críticos
       /----------\
      / Integration \      Moderados — bordas e integrações reais
     /----------------\
    /    Unit Tests     \  Muitos, rápidos, baratos — lógica de negócio
   /____________________\
```

## Padrão por tipo de código

### Lógica de negócio (domain)
- **Testes unitários** com alta cobertura
- **Property-based tests** para lógica complexa com muitos inputs
- Sem mocks de infraestrutura — teste a lógica pura

### Bordas HTTP (controllers/handlers)
- **Testes de integração** com servidor embarcado
- Validar: status codes, response body, headers, validação de input
- Testar: happy path, input inválido, erros de negócio, autenticação

### Persistência (repositories)
- **Testes de integração** com banco real (Testcontainers)
- Validar: CRUD, queries complexas, paginação, concorrência
- Nunca mock o banco para testar queries

### Mensageria (consumers/producers)
- **Testes de integração** com broker real (Testcontainers)
- Validar: consumo, idempotência, DLQ, serialização

### Clientes externos (HTTP clients)
- **Testes com WireMock/MockServer** — simule respostas
- Validar: sucesso, timeout, erro 4xx, erro 5xx, retry

## Padrões por linguagem

### Java (JUnit 5)
```java
@Test
void shouldRejectOrderWhenInsufficientStock() {
    // given
    var product = aProduct().withStock(5).build();
    var order = anOrder().withQuantity(10).build();
    
    // when/then
    assertThatThrownBy(() -> orderService.place(order))
        .isInstanceOf(InsufficientStockException.class);
}
```

### Python (pytest)
```python
@pytest.mark.parametrize("quantity,stock,expected", [
    (5, 10, True),
    (10, 10, True),
    (11, 10, False),
])
def test_can_fulfill_order(quantity, stock, expected):
    product = Product(stock=stock)
    assert product.can_fulfill(quantity) == expected
```

### Go (table-driven)
```go
func TestCanFulfillOrder(t *testing.T) {
    tests := []struct {
        name     string
        quantity int
        stock    int
        want     bool
    }{
        {"within stock", 5, 10, true},
        {"exact stock", 10, 10, true},
        {"exceeds stock", 11, 10, false},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            p := Product{Stock: tt.stock}
            got := p.CanFulfill(tt.quantity)
            assert.Equal(t, tt.want, got)
        })
    }
}
```

## Anti-patterns
- Testar implementação em vez de comportamento
- Mock de tudo — perde confiança na integração
- Testes frágeis que quebram com refactoring
- Testes sem assertions claras
- Testes que dependem de ordem de execução
- Testes que dependem de estado externo não controlado
