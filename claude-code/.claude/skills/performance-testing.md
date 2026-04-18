---
name: performance-testing
description: "Padrões de testes de performance: k6, Gatling, JMH, load testing, stress testing, benchmarking, profiling. Use quando planejar ou implementar testes de carga, benchmarks ou profiling."
---

# Performance Testing — Patterns & Tools

Padroes para testes de performance, carga e benchmarking em producao.

## Tipos de teste

| Tipo | Objetivo | Duracao | Carga |
|------|----------|---------|-------|
| **Load test** | Validar comportamento sob carga esperada | 10-30 min | Normal (SLO target) |
| **Stress test** | Encontrar ponto de quebra | 10-30 min | Crescente ate falhar |
| **Soak test** | Detectar memory leaks, degradacao | 2-8 horas | Carga constante moderada |
| **Spike test** | Validar auto-scaling e recuperacao | 5-15 min | Picos subitos |
| **Benchmark** | Medir performance de funcao/metodo | Segundos | N/A (micro) |

## k6 (Load testing HTTP)

```javascript
import http from "k6/http";
import { check, sleep } from "k6";
import { Rate, Trend } from "k6/metrics";

const errorRate = new Rate("errors");
const orderDuration = new Trend("order_duration", true);

export const options = {
  // Load test: ramp up, sustain, ramp down
  stages: [
    { duration: "2m", target: 50 },   // ramp up
    { duration: "10m", target: 50 },   // sustain
    { duration: "2m", target: 0 },     // ramp down
  ],
  thresholds: {
    http_req_duration: ["p(95)<500", "p(99)<1000"], // SLO: p95 < 500ms
    errors: ["rate<0.01"],                           // SLO: error rate < 1%
    order_duration: ["p(95)<800"],
  },
};

const BASE_URL = __ENV.BASE_URL || "http://localhost:8080";

export default function () {
  // List orders
  const listRes = http.get(`${BASE_URL}/api/v1/orders?page=0&size=20`);
  check(listRes, {
    "list status 200": (r) => r.status === 200,
    "list has orders": (r) => JSON.parse(r.body).length > 0,
  });
  errorRate.add(listRes.status !== 200);

  sleep(1);

  // Create order
  const createStart = Date.now();
  const createRes = http.post(
    `${BASE_URL}/api/v1/orders`,
    JSON.stringify({ title: `Order ${Date.now()}`, amount: 99.90 }),
    { headers: { "Content-Type": "application/json" } },
  );
  orderDuration.add(Date.now() - createStart);

  check(createRes, {
    "create status 201": (r) => r.status === 201,
    "create has id": (r) => JSON.parse(r.body).id !== undefined,
  });
  errorRate.add(createRes.status !== 201);

  sleep(1);
}

// Stress test variant
export const stressOptions = {
  stages: [
    { duration: "2m", target: 100 },
    { duration: "5m", target: 100 },
    { duration: "2m", target: 200 },
    { duration: "5m", target: 200 },
    { duration: "2m", target: 300 },
    { duration: "5m", target: 300 },
    { duration: "5m", target: 0 },
  ],
};

// Spike test variant
export const spikeOptions = {
  stages: [
    { duration: "1m", target: 10 },   // baseline
    { duration: "10s", target: 500 },  // spike
    { duration: "3m", target: 500 },   // sustain spike
    { duration: "10s", target: 10 },   // recover
    { duration: "3m", target: 10 },    // verify recovery
    { duration: "1m", target: 0 },
  ],
};
```

### k6 — Executar

```bash
# Load test
k6 run --env BASE_URL=http://localhost:8080 load-test.js

# Com output para Grafana/InfluxDB
k6 run --out influxdb=http://localhost:8086/k6 load-test.js

# Com output JSON
k6 run --out json=results.json load-test.js
```

## Gatling (JVM)

```scala
class OrderSimulation extends Simulation {

  val httpProtocol = http
    .baseUrl("http://localhost:8080")
    .acceptHeader("application/json")
    .contentTypeHeader("application/json")

  val listOrders = exec(
    http("List Orders")
      .get("/api/v1/orders?page=0&size=20")
      .check(status.is(200))
      .check(jsonPath("$[*]").count.gte(0))
  )

  val createOrder = exec(
    http("Create Order")
      .post("/api/v1/orders")
      .body(StringBody("""{"title":"Order #{counter}","amount":99.90}"""))
      .check(status.is(201))
      .check(jsonPath("$.id").saveAs("orderId"))
  )

  val getOrder = exec(
    http("Get Order")
      .get("/api/v1/orders/#{orderId}")
      .check(status.is(200))
  )

  val orderScenario = scenario("Order Flow")
    .exec(listOrders)
    .pause(1)
    .exec(createOrder)
    .pause(500.milliseconds)
    .exec(getOrder)

  setUp(
    orderScenario.inject(
      rampUsers(50).during(2.minutes),
      constantUsersPerSec(10).during(10.minutes),
    )
  ).protocols(httpProtocol)
    .assertions(
      global.responseTime.percentile(95).lt(500),
      global.successfulRequests.percent.gte(99.0),
    )
}
```

## JMH (Java Microbenchmark)

```java
@BenchmarkMode(Mode.AverageTime)
@OutputTimeUnit(TimeUnit.MICROSECONDS)
@State(Scope.Benchmark)
@Warmup(iterations = 3, time = 1)
@Measurement(iterations = 5, time = 1)
@Fork(1)
public class OrderMapperBenchmark {

    private Order order;
    private OrderMapper mapper;

    @Setup
    public void setup() {
        order = new Order("id-1", "Test Order", 99.90, OrderStatus.PENDING, Instant.now());
        mapper = new OrderMapper();
    }

    @Benchmark
    public OrderResponse mapOrder() {
        return mapper.toResponse(order);
    }

    @Benchmark
    public List<OrderResponse> mapOrders() {
        var orders = IntStream.range(0, 100).mapToObj(i -> order).toList();
        return orders.stream().map(mapper::toResponse).toList();
    }
}

// Executar: mvn verify -pl benchmarks
// ou: java -jar benchmarks.jar -rf json -rff results.json
```

## Go benchmarks

```go
func BenchmarkOrderMapper(b *testing.B) {
    order := &Order{ID: "1", Title: "Test", Amount: 99.90}
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        _ = toResponse(order)
    }
}

func BenchmarkOrderService_List(b *testing.B) {
    svc := setupTestService(b)
    ctx := context.Background()
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        _, _ = svc.List(ctx, "", 0, 20)
    }
}

// Executar: go test -bench=. -benchmem -benchtime=5s ./...
```

## Python — locust (alternativa a k6)

```python
from locust import HttpUser, task, between

class OrderUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def list_orders(self):
        self.client.get("/api/v1/orders?page=0&size=20")

    @task(1)
    def create_order(self):
        self.client.post("/api/v1/orders", json={"title": "Load Test", "amount": 99.90})

# Executar: locust -f locustfile.py --host=http://localhost:8080
```

## Profiling

### Java

```bash
# async-profiler (CPU + allocation)
java -agentpath:/path/to/libasyncProfiler.so=start,event=cpu,file=profile.html -jar app.jar

# JFR (Java Flight Recorder)
java -XX:StartFlightRecording=duration=60s,filename=recording.jfr -jar app.jar

# Heap dump
jmap -dump:format=b,file=heap.hprof <pid>
```

### Go

```go
import _ "net/http/pprof"

// Acessar: http://localhost:6060/debug/pprof/
// CPU: go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30
// Heap: go tool pprof http://localhost:6060/debug/pprof/heap
// Goroutines: go tool pprof http://localhost:6060/debug/pprof/goroutine
```

### Python

```bash
# cProfile
python -m cProfile -o output.prof app.py
# Visualizar: snakeviz output.prof

# py-spy (sampling, sem overhead)
py-spy record -o profile.svg -- python app.py
```

## SLOs como thresholds

```javascript
// k6 thresholds mapeados para SLOs reais
export const options = {
  thresholds: {
    // Availability SLO: 99.9%
    "checks": ["rate>0.999"],

    // Latency SLO: p95 < 500ms, p99 < 1s
    "http_req_duration": ["p(95)<500", "p(99)<1000"],

    // Error SLO: < 0.1%
    "http_req_failed": ["rate<0.001"],

    // Throughput SLO: > 100 rps
    "http_reqs": ["rate>100"],
  },
};
```

## Quando executar

| Momento | Tipo | Automatizado? |
|---------|------|--------------|
| PR com mudanca de performance | Benchmark (JMH/Go) | Sim (CI) |
| Pre-release | Load test | Sim (CD pipeline) |
| Pos-deploy staging | Smoke + load test | Sim |
| Mensal | Soak test | Agendado |
| Antes de evento de pico | Stress + spike | Manual |

## Checklist

- [ ] Load test com thresholds mapeados para SLOs?
- [ ] Stress test para encontrar ponto de quebra?
- [ ] Soak test para detectar memory leaks?
- [ ] Microbenchmarks para hot paths (JMH, Go bench)?
- [ ] Profiling disponivel em staging (pprof, JFR)?
- [ ] Resultados comparaveis entre execucoes (baseline)?
- [ ] Thresholds no CI para regressao de performance?
- [ ] Cenarios realistas (nao so endpoints isolados)?
- [ ] Dados de teste representativos do volume real?
- [ ] Dashboard para visualizar resultados historicos?
