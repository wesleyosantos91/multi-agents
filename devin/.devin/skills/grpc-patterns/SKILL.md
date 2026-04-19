---
name: grpc-patterns
description: "Padrões gRPC: Protobuf, service definition, streaming, deadlines, interceptors, error handling, testing. Use quando implementar ou revisar APIs gRPC."
argument-hint: "[contexto adicional]"
---

# gRPC — Patterns & Idioms

Padroes e idiomas para gRPC em producao.

## Quando usar gRPC vs REST

| Criterio | gRPC | REST |
|----------|------|------|
| Comunicacao interna (service-to-service) | Preferido | OK |
| API publica / browser | Nao (precisa grpc-web) | Preferido |
| Streaming bidirecional | Sim (nativo) | Nao (WebSocket) |
| Performance / baixa latencia | Melhor (binario, HTTP/2) | Bom |
| Schema first / contrato forte | Sim (Protobuf) | Sim (OpenAPI) |
| Ecossistema / tooling browser | Limitado | Amplo |

## Protobuf — Schema first

```protobuf
syntax = "proto3";
package order.v1;

option java_package = "com.example.order.grpc";
option java_multiple_files = true;
option go_package = "github.com/example/order/gen/orderv1";

import "google/protobuf/timestamp.proto";
import "google/protobuf/field_mask.proto";

// Service definition
service OrderService {
  // Unary
  rpc GetOrder(GetOrderRequest) returns (Order);
  rpc CreateOrder(CreateOrderRequest) returns (Order);
  rpc ListOrders(ListOrdersRequest) returns (ListOrdersResponse);
  rpc UpdateOrder(UpdateOrderRequest) returns (Order);
  rpc DeleteOrder(DeleteOrderRequest) returns (google.protobuf.Empty);

  // Server streaming
  rpc WatchOrders(WatchOrdersRequest) returns (stream OrderEvent);

  // Client streaming
  rpc BatchCreateOrders(stream CreateOrderRequest) returns (BatchCreateResponse);
}

// Messages
message Order {
  string id = 1;
  string title = 2;
  double amount = 3;
  OrderStatus status = 4;
  google.protobuf.Timestamp created_at = 5;
  google.protobuf.Timestamp updated_at = 6;
}

enum OrderStatus {
  ORDER_STATUS_UNSPECIFIED = 0;
  ORDER_STATUS_PENDING = 1;
  ORDER_STATUS_CONFIRMED = 2;
  ORDER_STATUS_SHIPPED = 3;
  ORDER_STATUS_DELIVERED = 4;
  ORDER_STATUS_CANCELLED = 5;
}

message GetOrderRequest {
  string id = 1;
}

message CreateOrderRequest {
  string title = 1;
  double amount = 2;
  string description = 3;
}

message ListOrdersRequest {
  int32 page_size = 1;    // max 100
  string page_token = 2;  // cursor-based pagination
  string filter = 3;      // e.g. "status=PENDING"
  string order_by = 4;    // e.g. "created_at desc"
}

message ListOrdersResponse {
  repeated Order orders = 1;
  string next_page_token = 2;
  int32 total_size = 3;
}

message UpdateOrderRequest {
  Order order = 1;
  google.protobuf.FieldMask update_mask = 2;
}
```

## Backward compatibility — Regras

- **NUNCA** remover ou renumerar campos existentes
- **NUNCA** mudar o tipo de um campo existente
- Campos removidos: marcar como `reserved`
- Novos campos: usar o proximo numero disponivel
- Enums: `UNSPECIFIED = 0` sempre como primeiro valor

```protobuf
message Order {
  string id = 1;
  // campo removido — reservar para nao reusar
  reserved 7;
  reserved "old_field_name";
}
```

## Java (Spring Boot + grpc-spring-boot-starter)

```java
@GrpcService
public class OrderGrpcService extends OrderServiceGrpc.OrderServiceImplBase {

    private final OrderService orderService;

    @Override
    public void getOrder(GetOrderRequest request, StreamObserver<Order> responseObserver) {
        try {
            var order = orderService.findById(request.getId())
                .orElseThrow(() -> Status.NOT_FOUND
                    .withDescription("Order not found: " + request.getId())
                    .asRuntimeException());

            responseObserver.onNext(toProto(order));
            responseObserver.onCompleted();
        } catch (StatusRuntimeException e) {
            responseObserver.onError(e);
        }
    }

    @Override
    public void listOrders(ListOrdersRequest request, StreamObserver<ListOrdersResponse> responseObserver) {
        var result = orderService.list(request.getPageSize(), request.getPageToken());
        responseObserver.onNext(ListOrdersResponse.newBuilder()
            .addAllOrders(result.items().stream().map(this::toProto).toList())
            .setNextPageToken(result.nextToken())
            .setTotalSize(result.total())
            .build());
        responseObserver.onCompleted();
    }
}
```

## Go

```go
type orderServer struct {
    orderv1.UnimplementedOrderServiceServer
    service OrderService
}

func (s *orderServer) GetOrder(ctx context.Context, req *orderv1.GetOrderRequest) (*orderv1.Order, error) {
    order, err := s.service.FindByID(ctx, req.GetId())
    if err != nil {
        if errors.Is(err, ErrNotFound) {
            return nil, status.Errorf(codes.NotFound, "order not found: %s", req.GetId())
        }
        return nil, status.Errorf(codes.Internal, "internal error")
    }
    return toProto(order), nil
}

func (s *orderServer) WatchOrders(req *orderv1.WatchOrdersRequest, stream orderv1.OrderService_WatchOrdersServer) error {
    ctx := stream.Context()
    ch := s.service.Subscribe(ctx, req.GetFilter())
    for {
        select {
        case <-ctx.Done():
            return nil
        case event, ok := <-ch:
            if !ok { return nil }
            if err := stream.Send(toEventProto(event)); err != nil {
                return err
            }
        }
    }
}
```

## Python

```python
class OrderServicer(order_pb2_grpc.OrderServiceServicer):
    def __init__(self, service: OrderService):
        self.service = service

    async def GetOrder(self, request, context):
        order = await self.service.find_by_id(request.id)
        if not order:
            context.abort(grpc.StatusCode.NOT_FOUND, f"Order not found: {request.id}")
        return to_proto(order)

    async def ListOrders(self, request, context):
        result = await self.service.list(page_size=request.page_size, page_token=request.page_token)
        return order_pb2.ListOrdersResponse(
            orders=[to_proto(o) for o in result.items],
            next_page_token=result.next_token,
            total_size=result.total,
        )
```

## Interceptors (middleware)

```java
// Java — Server interceptor
@Component
public class LoggingInterceptor implements ServerInterceptor {
    @Override
    public <T, R> ServerCall.Listener<T> interceptCall(
        ServerCall<T, R> call, Metadata headers, ServerCallHandler<T, R> next
    ) {
        var start = System.nanoTime();
        var method = call.getMethodDescriptor().getFullMethodName();
        slog.info("grpc.request", "method", method);

        return next.startCall(new ForwardingServerCall.SimpleForwardingServerCall<>(call) {
            @Override
            public void close(Status status, Metadata trailers) {
                var duration = Duration.ofNanos(System.nanoTime() - start);
                slog.info("grpc.response", "method", method, "status", status.getCode(), "duration_ms", duration.toMillis());
                super.close(status, trailers);
            }
        }, headers);
    }
}
```

## Deadlines e timeouts

```java
// Client — sempre definir deadline
OrderServiceGrpc.OrderServiceBlockingStub stub = OrderServiceGrpc.newBlockingStub(channel)
    .withDeadlineAfter(5, TimeUnit.SECONDS);

// Server — checar se deadline expirou
if (Context.current().isCancelled()) {
    responseObserver.onError(Status.CANCELLED.withDescription("Deadline exceeded").asRuntimeException());
    return;
}
```

```go
// Go client
ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
defer cancel()
order, err := client.GetOrder(ctx, &orderv1.GetOrderRequest{Id: "123"})
```

## Error handling — Status codes

| gRPC Code | Quando usar | HTTP equiv |
|-----------|-------------|-----------|
| `OK` | Sucesso | 200 |
| `NOT_FOUND` | Recurso nao existe | 404 |
| `ALREADY_EXISTS` | Conflito de criacao | 409 |
| `INVALID_ARGUMENT` | Input invalido | 400 |
| `PERMISSION_DENIED` | Sem permissao | 403 |
| `UNAUTHENTICATED` | Sem auth | 401 |
| `DEADLINE_EXCEEDED` | Timeout | 504 |
| `UNAVAILABLE` | Servico indisponivel (retry) | 503 |
| `INTERNAL` | Erro interno (nao retry) | 500 |

## Testing

```java
@ExtendWith(GrpcCleanupExtension.class)
class OrderGrpcServiceTest {
    @RegisterExtension
    static GrpcServerExtension grpcServer = new GrpcServerExtension();

    @Test
    void shouldGetOrder() {
        var stub = OrderServiceGrpc.newBlockingStub(grpcServer.getChannel());
        var response = stub.getOrder(GetOrderRequest.newBuilder().setId("1").build());
        assertThat(response.getTitle()).isEqualTo("Test Order");
    }

    @Test
    void shouldReturnNotFound() {
        var stub = OrderServiceGrpc.newBlockingStub(grpcServer.getChannel());
        var exception = assertThrows(StatusRuntimeException.class,
            () -> stub.getOrder(GetOrderRequest.newBuilder().setId("nonexistent").build()));
        assertThat(exception.getStatus().getCode()).isEqualTo(Status.Code.NOT_FOUND);
    }
}
```

## Checklist

- [ ] Protobuf como fonte verdade do contrato?
- [ ] Backward compatibility (sem remover/renumerar campos)?
- [ ] `UNSPECIFIED = 0` em todos os enums?
- [ ] Campos removidos marcados como `reserved`?
- [ ] Deadlines/timeouts em todas as chamadas client?
- [ ] Error handling com status codes corretos?
- [ ] Interceptors para logging, auth, metrics?
- [ ] Cursor-based pagination (page_token)?
- [ ] FieldMask para updates parciais?
- [ ] Testes de integracao com server in-process?
