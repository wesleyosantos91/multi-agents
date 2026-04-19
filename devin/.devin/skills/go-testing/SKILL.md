---
name: go-testing
description: "Testes Go: table-driven, subtests, testcontainers, mocks, benchmarks e race detection. Use quando criar testes Go ou melhorar cobertura em projetos Go."
argument-hint: "[contexto adicional]"
---

# Go Testing — Idiomatic Patterns

Guia de testes idiomáticos para Go.

## Table-driven tests (padrão)
```go
func TestCalculateDiscount(t *testing.T) {
    tests := []struct {
        name     string
        amount   float64
        tier     CustomerTier
        want     float64
        wantErr  bool
    }{
        {"standard no discount", 100, Standard, 100, false},
        {"premium 10% off", 100, Premium, 90, false},
        {"vip 20% off", 100, VIP, 80, false},
        {"zero amount", 0, Premium, 0, false},
        {"negative amount errors", -1, Standard, 0, true},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := CalculateDiscount(tt.amount, tt.tier)
            if tt.wantErr {
                assert.Error(t, err)
                return
            }
            assert.NoError(t, err)
            assert.InDelta(t, tt.want, got, 0.01)
        })
    }
}
```

## Subtests para setup complexo
```go
func TestOrderService(t *testing.T) {
    repo := newMockOrderRepo()
    svc := NewOrderService(repo)

    t.Run("Create", func(t *testing.T) {
        t.Run("should create valid order", func(t *testing.T) {
            order, err := svc.Create(context.Background(), validOrderRequest())
            assert.NoError(t, err)
            assert.Equal(t, StatusPending, order.Status)
        })

        t.Run("should reject empty items", func(t *testing.T) {
            req := validOrderRequest()
            req.Items = nil
            _, err := svc.Create(context.Background(), req)
            assert.ErrorIs(t, err, ErrEmptyItems)
        })
    })

    t.Run("Cancel", func(t *testing.T) {
        t.Run("should cancel pending order", func(t *testing.T) {
            order := repo.seedPendingOrder()
            err := svc.Cancel(context.Background(), order.ID)
            assert.NoError(t, err)
        })

        t.Run("should reject cancel of shipped order", func(t *testing.T) {
            order := repo.seedShippedOrder()
            err := svc.Cancel(context.Background(), order.ID)
            var notCancellable *OrderNotCancellableError
            assert.ErrorAs(t, err, &notCancellable)
        })
    })
}
```

## Mocks com interface
```go
// Interface no ponto de uso
type OrderRepository interface {
    FindByID(ctx context.Context, id string) (*Order, error)
    Save(ctx context.Context, order *Order) error
}

// Mock manual (preferido em Go vs frameworks de mock)
type mockOrderRepo struct {
    orders map[string]*Order
    saveErr error
}

func newMockOrderRepo() *mockOrderRepo {
    return &mockOrderRepo{orders: make(map[string]*Order)}
}

func (m *mockOrderRepo) FindByID(_ context.Context, id string) (*Order, error) {
    order, ok := m.orders[id]
    if !ok {
        return nil, &OrderNotFoundError{ID: id}
    }
    return order, nil
}

func (m *mockOrderRepo) Save(_ context.Context, order *Order) error {
    if m.saveErr != nil {
        return m.saveErr
    }
    m.orders[order.ID] = order
    return nil
}

func (m *mockOrderRepo) seedPendingOrder() *Order {
    o := &Order{ID: "ord-1", Status: StatusPending}
    m.orders[o.ID] = o
    return o
}
```

## Testes de integração (Testcontainers)
```go
func TestOrderRepository_Postgres(t *testing.T) {
    if testing.Short() {
        t.Skip("skipping integration test")
    }

    ctx := context.Background()
    container, err := postgres.Run(ctx,
        "postgres:16-alpine",
        postgres.WithDatabase("test"),
        postgres.WithUsername("test"),
        postgres.WithPassword("test"),
        testcontainers.WithWaitStrategy(
            wait.ForLog("database system is ready").WithStartupTimeout(30*time.Second)),
    )
    require.NoError(t, err)
    t.Cleanup(func() { container.Terminate(ctx) })

    connStr, err := container.ConnectionString(ctx, "sslmode=disable")
    require.NoError(t, err)

    db, err := sql.Open("postgres", connStr)
    require.NoError(t, err)
    defer db.Close()

    // run migrations
    runMigrations(t, db)

    repo := NewPostgresOrderRepository(db)

    t.Run("save and find", func(t *testing.T) {
        order := &Order{ID: uuid.New().String(), CustomerID: "cust-1", Status: StatusPending}
        err := repo.Save(ctx, order)
        assert.NoError(t, err)

        found, err := repo.FindByID(ctx, order.ID)
        assert.NoError(t, err)
        assert.Equal(t, order.CustomerID, found.CustomerID)
    })
}
```

## HTTP handler tests
```go
func TestGetOrderHandler(t *testing.T) {
    repo := newMockOrderRepo()
    repo.seedPendingOrder()
    handler := NewOrderHandler(NewOrderService(repo))

    t.Run("returns order when found", func(t *testing.T) {
        req := httptest.NewRequest(http.MethodGet, "/api/v1/orders/ord-1", nil)
        rec := httptest.NewRecorder()

        r := chi.NewRouter()
        r.Get("/api/v1/orders/{id}", handler.GetOrder)
        r.ServeHTTP(rec, req)

        assert.Equal(t, http.StatusOK, rec.Code)
        var resp OrderResponse
        json.NewDecoder(rec.Body).Decode(&resp)
        assert.Equal(t, "ord-1", resp.ID)
    })

    t.Run("returns 404 when not found", func(t *testing.T) {
        req := httptest.NewRequest(http.MethodGet, "/api/v1/orders/missing", nil)
        rec := httptest.NewRecorder()

        r := chi.NewRouter()
        r.Get("/api/v1/orders/{id}", handler.GetOrder)
        r.ServeHTTP(rec, req)

        assert.Equal(t, http.StatusNotFound, rec.Code)
    })
}
```

## Benchmarks
```go
func BenchmarkCalculateDiscount(b *testing.B) {
    for i := 0; i < b.N; i++ {
        CalculateDiscount(100.0, Premium)
    }
}

// Rodar: go test -bench=. -benchmem ./...
```

## Race detection
```bash
# SEMPRE em CI
go test -race ./...
```

## Comandos
```bash
go test ./...                    # rodar todos
go test -race ./...              # com race detector
go test -short ./...             # pular integração
go test -cover ./...             # com cobertura
go test -run TestCreate ./...    # filtrar por nome
go test -bench=. -benchmem ./...  # benchmarks
go test -v ./internal/service/   # verbose em um pacote
```

## Checklist
- [ ] Table-driven tests para casos múltiplos?
- [ ] Subtests com `t.Run` para organização?
- [ ] Mocks via interface (não framework)?
- [ ] `-race` em CI?
- [ ] `-short` para pular integração em dev rápido?
- [ ] Testcontainers para banco real em integração?
- [ ] HTTP tests com httptest?
- [ ] Benchmarks para código performance-critical?
