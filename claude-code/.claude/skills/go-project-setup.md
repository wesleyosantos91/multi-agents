---
name: go-project-setup
description: "Estrutura e setup de projetos Go idiomáticos. Use quando criar projeto Go, configurar módulo, ou revisar estrutura Go."
---

# Go Project Setup — Idiomatic Best Practices

Guia para estruturar projetos Go seguindo convenções da comunidade.

## Estrutura de projeto

### Serviço HTTP / API
```
myservice/
├── cmd/
│   └── server/
│       └── main.go            # Entrypoint — wiring e inicialização
├── internal/
│   ├── domain/
│   │   ├── order.go           # Entidades e regras de negócio
│   │   ├── order_test.go
│   │   └── repository.go      # Interfaces de persistência
│   ├── handler/
│   │   ├── order.go           # HTTP handlers
│   │   └── order_test.go
│   ├── service/
│   │   ├── order.go           # Lógica de aplicação
│   │   └── order_test.go
│   ├── repository/
│   │   ├── postgres/
│   │   │   ├── order.go       # Implementação PostgreSQL
│   │   │   └── order_test.go
│   │   └── dynamodb/
│   │       └── order.go       # Implementação DynamoDB
│   └── config/
│       └── config.go          # Configuração da aplicação
├── pkg/                       # Só se houver reuso externo REAL
├── go.mod
├── go.sum
├── Makefile
└── Dockerfile
```

### Lambda function
```
lambda-go/
├── cmd/
│   └── handler/
│       └── main.go            # Lambda entrypoint
├── internal/
│   ├── domain/                # Lógica de negócio (testável sem AWS)
│   ├── handler/               # Handler que recebe evento
│   └── adapter/               # Integrações (DynamoDB, SQS, etc)
├── go.mod
├── go.sum
├── Makefile
└── Dockerfile
```

## Regras idiomáticas

### Interfaces no ponto de uso
```go
// ERRADO — interface no pacote que implementa
// repository/order.go
type OrderRepository interface { ... }
type postgresOrderRepo struct { ... }

// CORRETO — interface no pacote que consome
// service/order.go
type OrderRepository interface {
    FindByID(ctx context.Context, id string) (*domain.Order, error)
    Save(ctx context.Context, order *domain.Order) error
}

type OrderService struct {
    repo OrderRepository  // depende da interface, não da implementação
}
```

### Context propagation
```go
// SEMPRE receber context como primeiro parâmetro
func (s *OrderService) Process(ctx context.Context, orderID string) error {
    order, err := s.repo.FindByID(ctx, orderID)
    if err != nil {
        return fmt.Errorf("finding order %s: %w", orderID, err)
    }
    // ...
}
```

### Error handling
```go
// Erros de domínio tipados
type OrderNotFoundError struct {
    ID string
}

func (e *OrderNotFoundError) Error() string {
    return fmt.Sprintf("order %s not found", e.ID)
}

// Wrap com contexto — SEMPRE
result, err := s.repo.Save(ctx, order)
if err != nil {
    return fmt.Errorf("saving order %s: %w", order.ID, err)
}

// Check por tipo — usar errors.As
var notFound *OrderNotFoundError
if errors.As(err, &notFound) {
    // handle not found
}
```

### Struct initialization
```go
// Functional options para structs complexas
type Server struct {
    addr    string
    timeout time.Duration
    logger  *slog.Logger
}

type Option func(*Server)

func WithTimeout(d time.Duration) Option {
    return func(s *Server) { s.timeout = d }
}

func NewServer(addr string, opts ...Option) *Server {
    s := &Server{addr: addr, timeout: 30 * time.Second, logger: slog.Default()}
    for _, opt := range opts {
        opt(s)
    }
    return s
}
```

### Logging (slog — stdlib)
```go
logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{Level: slog.LevelInfo}))

logger.Info("order created",
    slog.String("orderId", order.ID),
    slog.String("customerId", order.CustomerID),
    slog.Duration("duration", elapsed),
)
```

## Configuration
```go
type Config struct {
    Port        int           `env:"PORT" envDefault:"8080"`
    DatabaseURL string        `env:"DATABASE_URL,required"`
    Timeout     time.Duration `env:"TIMEOUT" envDefault:"30s"`
    LogLevel    string        `env:"LOG_LEVEL" envDefault:"info"`
}

// Usar: github.com/caarlos0/env/v11
func LoadConfig() (*Config, error) {
    cfg := &Config{}
    if err := env.Parse(cfg); err != nil {
        return nil, fmt.Errorf("parsing config: %w", err)
    }
    return cfg, nil
}
```

## HTTP Server (stdlib + chi/echo)
```go
func main() {
    cfg, err := config.LoadConfig()
    if err != nil {
        slog.Error("failed to load config", "error", err)
        os.Exit(1)
    }

    // Wiring
    repo := postgres.NewOrderRepository(db)
    svc := service.NewOrderService(repo)
    h := handler.NewOrderHandler(svc)

    // Router
    r := chi.NewRouter()
    r.Use(middleware.RequestID, middleware.RealIP, middleware.Logger, middleware.Recoverer)
    r.Route("/api/v1", func(r chi.Router) {
        r.Get("/orders/{id}", h.GetOrder)
        r.Post("/orders", h.CreateOrder)
    })
    r.Get("/health", func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
    })

    // Graceful shutdown
    srv := &http.Server{Addr: fmt.Sprintf(":%d", cfg.Port), Handler: r}
    go func() {
        if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            slog.Error("server error", "error", err)
        }
    }()

    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit
    ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
    defer cancel()
    srv.Shutdown(ctx)
}
```

## Makefile
```makefile
.PHONY: build test lint run

build:
	go build -ldflags="-s -w" -o bin/server ./cmd/server

test:
	go test -race -cover ./...

lint:
	golangci-lint run ./...

run:
	go run ./cmd/server
```

## Checklist
- [ ] `cmd/` para entrypoints, `internal/` para código privado?
- [ ] `pkg/` somente com reuso externo justificado?
- [ ] Interfaces no ponto de uso (não no implementador)?
- [ ] `context.Context` como primeiro parâmetro?
- [ ] Erros wrapped com `fmt.Errorf("context: %w", err)`?
- [ ] Sem `panic` como controle de fluxo?
- [ ] `slog` para logging estruturado?
- [ ] Graceful shutdown implementado?
- [ ] Makefile com targets: build, test, lint, run?
- [ ] golangci-lint configurado?
