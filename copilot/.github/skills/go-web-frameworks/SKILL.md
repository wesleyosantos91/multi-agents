---
name: go-web-frameworks
description: Skill importada do EXEMPLO (go-web-frameworks.md).
allowed-tools: "read,search"
user-invocable: true
---

# Skill

---
name: go-web-frameworks
description: "Padrões de frameworks web Go: Gin, Chi, Echo. Routing, middleware, validation, graceful shutdown, structured logging. Use quando implementar APIs HTTP em Go."
---

# Go Web Frameworks — Gin, Chi, Echo

Padroes e idiomas para frameworks web Go em producao.

## Escolha de framework

| Framework | Quando usar | Filosofia |
|-----------|-------------|-----------|
| **Chi** | APIs que precisam de compatibilidade `net/http` | Leve, stdlib-compatible, middleware composavel |
| **Gin** | APIs com alta performance e ecossistema maduro | Rapido, binding/validation, middleware chain |
| **Echo** | APIs com middleware rico e documentacao OpenAPI | Ergonomico, extensivel, middleware built-in |
| **stdlib** (`net/http`) | APIs simples, sem dependencia externa | Go 1.22+ com routing melhorado |

## Chi

```go
package main

import (
    "net/http"
    "github.com/go-chi/chi/v5"
    "github.com/go-chi/chi/v5/middleware"
)

func main() {
    r := chi.NewRouter()

    // Middleware stack
    r.Use(middleware.RequestID)
    r.Use(middleware.RealIP)
    r.Use(middleware.Logger)
    r.Use(middleware.Recoverer)
    r.Use(middleware.Timeout(30 * time.Second))

    // Routes
    r.Route("/api/v1", func(r chi.Router) {
        r.Route("/orders", func(r chi.Router) {
            r.Get("/", listOrders)
            r.Post("/", createOrder)
            r.Route("/{id}", func(r chi.Router) {
                r.Use(orderCtx) // middleware de contexto
                r.Get("/", getOrder)
                r.Put("/", updateOrder)
                r.Delete("/", deleteOrder)
            })
        })
    })

    // Health
    r.Get("/health", func(w http.ResponseWriter, r *http.Request) {
        w.WriteHeader(http.StatusOK)
    })

    srv := &http.Server{Addr: ":8080", Handler: r}
    gracefulShutdown(srv)
}
```

### Chi — Handler idiomatico

```go
func listOrders(w http.ResponseWriter, r *http.Request) {
    ctx := r.Context()

    status := r.URL.Query().Get("status")
    page, _ := strconv.Atoi(r.URL.Query().Get("page"))
    size, _ := strconv.Atoi(r.URL.Query().Get("size"))
    if size == 0 { size = 20 }

    orders, err := orderService.List(ctx, status, page, size)
    if err != nil {
        respondError(w, r, err)
        return
    }

    respondJSON(w, http.StatusOK, orders)
}

func getOrder(w http.ResponseWriter, r *http.Request) {
    order := r.Context().Value(orderKey).(*Order) // do middleware orderCtx
    respondJSON(w, http.StatusOK, order)
}

// Middleware de contexto
func orderCtx(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        id := chi.URLParam(r, "id")
        order, err := orderService.FindByID(r.Context(), id)
        if err != nil {
            respondError(w, r, ErrNotFound)
            return
        }
        ctx := context.WithValue(r.Context(), orderKey, order)
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}
```

## Gin

```go
func main() {
    r := gin.New()

    // Middleware
    r.Use(gin.Recovery())
    r.Use(requestIDMiddleware())
    r.Use(structuredLogger())
    r.Use(timeoutMiddleware(30 * time.Second))

    // Routes
    v1 := r.Group("/api/v1")
    {
        orders := v1.Group("/orders")
        {
            orders.GET("", listOrders)
            orders.POST("", createOrder)
            orders.GET("/:id", getOrder)
            orders.PUT("/:id", updateOrder)
            orders.DELETE("/:id", deleteOrder)
        }
    }

    r.GET("/health", func(c *gin.Context) {
        c.Status(http.StatusOK)
    })

    srv := &http.Server{Addr: ":8080", Handler: r}
    gracefulShutdown(srv)
}
```

### Gin — Handler idiomatico

```go
func listOrders(c *gin.Context) {
    var query ListOrdersQuery
    if err := c.ShouldBindQuery(&query); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    orders, err := orderService.List(c.Request.Context(), query)
    if err != nil {
        handleError(c, err)
        return
    }

    c.JSON(http.StatusOK, orders)
}

func createOrder(c *gin.Context) {
    var req CreateOrderRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    order, err := orderService.Create(c.Request.Context(), req)
    if err != nil {
        handleError(c, err)
        return
    }

    c.JSON(http.StatusCreated, order)
}

// Binding + Validation
type CreateOrderRequest struct {
    Title       string  `json:"title" binding:"required,max=100"`
    Amount      float64 `json:"amount" binding:"required,gt=0"`
    Description string  `json:"description" binding:"max=500"`
}

type ListOrdersQuery struct {
    Status string `form:"status"`
    Page   int    `form:"page,default=0"`
    Size   int    `form:"size,default=20" binding:"max=100"`
}
```

## Echo

```go
func main() {
    e := echo.New()

    // Middleware
    e.Use(emiddleware.RequestID())
    e.Use(emiddleware.Recover())
    e.Use(emiddleware.TimeoutWithConfig(emiddleware.TimeoutConfig{Timeout: 30 * time.Second}))
    e.Use(structuredLogger())

    // Routes
    v1 := e.Group("/api/v1")
    orders := v1.Group("/orders")
    orders.GET("", listOrders)
    orders.POST("", createOrder)
    orders.GET("/:id", getOrder)

    e.GET("/health", func(c echo.Context) error {
        return c.NoContent(http.StatusOK)
    })

    gracefulShutdown(e)
}

func createOrder(c echo.Context) error {
    var req CreateOrderRequest
    if err := c.Bind(&req); err != nil {
        return echo.NewHTTPError(http.StatusBadRequest, err.Error())
    }
    if err := c.Validate(&req); err != nil {
        return echo.NewHTTPError(http.StatusBadRequest, err.Error())
    }

    order, err := orderService.Create(c.Request().Context(), req)
    if err != nil {
        return err // centralizado no error handler
    }

    return c.JSON(http.StatusCreated, order)
}
```

## Middleware padrao (qualquer framework)

```go
// Request ID
func requestIDMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        id := c.GetHeader("X-Request-ID")
        if id == "" {
            id = uuid.NewString()
        }
        c.Set("request_id", id)
        c.Header("X-Request-ID", id)
        c.Next()
    }
}

// Structured logging middleware
func structuredLogger() gin.HandlerFunc {
    return func(c *gin.Context) {
        start := time.Now()
        c.Next()
        slog.Info("request",
            "method", c.Request.Method,
            "path", c.Request.URL.Path,
            "status", c.Writer.Status(),
            "duration_ms", time.Since(start).Milliseconds(),
            "request_id", c.GetString("request_id"),
        )
    }
}
```

## Error handling centralizado

```go
// Domain errors
var (
    ErrNotFound     = &AppError{Code: http.StatusNotFound, Type: "not_found", Message: "resource not found"}
    ErrConflict     = &AppError{Code: http.StatusConflict, Type: "conflict", Message: "resource already exists"}
    ErrValidation   = &AppError{Code: http.StatusUnprocessableEntity, Type: "validation_error"}
)

type AppError struct {
    Code    int    `json:"-"`
    Type    string `json:"type"`
    Message string `json:"detail"`
}

func (e *AppError) Error() string { return e.Message }

func handleError(c *gin.Context, err error) {
    var appErr *AppError
    if errors.As(err, &appErr) {
        c.JSON(appErr.Code, appErr)
        return
    }
    slog.Error("unhandled error", "error", err)
    c.JSON(http.StatusInternalServerError, gin.H{"type": "internal", "detail": "internal server error"})
}
```

## Graceful shutdown

```go
func gracefulShutdown(srv *http.Server) {
    go func() {
        if err := srv.ListenAndServe(); err != nil && !errors.Is(err, http.ErrServerClosed) {
            slog.Error("server error", "error", err)
            os.Exit(1)
        }
    }()

    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit

    slog.Info("shutting down server")
    ctx, cancel := context.WithTimeout(context.Background(), 15*time.Second)
    defer cancel()

    if err := srv.Shutdown(ctx); err != nil {
        slog.Error("forced shutdown", "error", err)
    }
}
```

## Validation (go-playground/validator)

```go
import "github.com/go-playground/validator/v10"

var validate = validator.New()

type CreateOrderRequest struct {
    Title  string  `json:"title" validate:"required,min=1,max=100"`
    Amount float64 `json:"amount" validate:"required,gt=0"`
    Email  string  `json:"email" validate:"required,email"`
}

func validateStruct(s any) error {
    return validate.Struct(s)
}
```

## Checklist

- [ ] Graceful shutdown com signal handling?
- [ ] Request ID propagado via middleware?
- [ ] Timeout middleware configurado?
- [ ] Recovery/panic handler?
- [ ] Structured logging (slog) no middleware?
- [ ] Error handling centralizado com tipos de dominio?
- [ ] Validation com go-playground/validator ou equivalente?
- [ ] Health endpoint (/health ou /healthz)?
- [ ] Context propagado para service/repository?
- [ ] Binding tipado para query params e body?
