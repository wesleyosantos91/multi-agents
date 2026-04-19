---
name: performance-testing
description: "Padrões de testes de performance: k6, Gatling, JMeter, JMH, load/stress/soak testing, benchmarking, profiling. Use quando planejar ou implementar testes de carga, benchmarks ou profiling."
argument-hint: "[contexto adicional]"
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

## Escolha de ferramenta

| Criterio | k6 | Gatling | JMeter | Locust |
|----------|-----|---------|--------|--------|
| Linguagem | JavaScript | Scala | GUI + Groovy | Python |
| HTTP | Sim | Sim | Sim | Sim |
| JDBC/JMS/LDAP | Nao | Nao | **Sim** | Nao |
| gRPC | Nativo | Plugin | Plugin | Plugin |
| GUI para design | Nao | Nao | **Sim** | Nao |
| CI/CD headless | Sim | Sim | Sim (CLI) | Sim |
| Distributed | k6 Cloud | Nao | **Nativo** | Nativo |
| Melhor para | APIs HTTP/gRPC | JVM teams | Multi-protocolo, Java teams | Python teams |

## k6 (Load testing HTTP — recomendado para APIs)

```javascript
import http from "k6/http";
import { check, sleep } from "k6";
import { Rate, Trend } from "k6/metrics";

const errorRate = new Rate("errors");
const orderDuration = new Trend("order_duration", true);

export const options = {
  stages: [
    { duration: "2m", target: 50 },   // ramp up
    { duration: "10m", target: 50 },   // sustain
    { duration: "2m", target: 0 },     // ramp down
  ],
  thresholds: {
    http_req_duration: ["p(95)<500", "p(99)<1000"],
    errors: ["rate<0.01"],
    order_duration: ["p(95)<800"],
  },
};

const BASE_URL = __ENV.BASE_URL || "http://localhost:8080";

export default function () {
  const listRes = http.get(`${BASE_URL}/api/v1/orders?page=0&size=20`);
  check(listRes, {
    "list status 200": (r) => r.status === 200,
    "list has orders": (r) => JSON.parse(r.body).length > 0,
  });
  errorRate.add(listRes.status !== 200);

  sleep(1);

  const createStart = Date.now();
  const createRes = http.post(
    `${BASE_URL}/api/v1/orders`,
    JSON.stringify({ title: `Order ${Date.now()}`, amount: 99.90 }),
    { headers: { "Content-Type": "application/json" } },
  );
  orderDuration.add(Date.now() - createStart);
  check(createRes, { "create status 201": (r) => r.status === 201 });
  errorRate.add(createRes.status !== 201);

  sleep(1);
}
```

```bash
# Executar
k6 run --env BASE_URL=http://localhost:8080 load-test.js

# Com output para Grafana/InfluxDB
k6 run --out influxdb=http://localhost:8086/k6 load-test.js
```

## Gatling (JVM teams)

```scala
class OrderSimulation extends Simulation {
  val httpProtocol = http
    .baseUrl("http://localhost:8080")
    .acceptHeader("application/json")
    .contentTypeHeader("application/json")

  val orderScenario = scenario("Order Flow")
    .exec(http("List Orders").get("/api/v1/orders?page=0&size=20").check(status.is(200)))
    .pause(1)
    .exec(http("Create Order").post("/api/v1/orders")
      .body(StringBody("""{"title":"Order #{counter}","amount":99.90}"""))
      .check(status.is(201)).check(jsonPath("$.id").saveAs("orderId")))
    .pause(500.milliseconds)
    .exec(http("Get Order").get("/api/v1/orders/#{orderId}").check(status.is(200)))

  setUp(
    orderScenario.inject(rampUsers(50).during(2.minutes), constantUsersPerSec(10).during(10.minutes))
  ).protocols(httpProtocol)
    .assertions(global.responseTime.percentile(95).lt(500), global.successfulRequests.percent.gte(99.0))
}
```

## JMeter (multi-protocolo, Java teams)

Usar JMeter quando: protocolo nao-HTTP (JDBC, JMS, LDAP), GUI para design de cenarios, ou testes distribuidos nativos.

### Estrutura de Test Plan

```
Test Plan
├── User Defined Variables          # BASE_URL, credenciais
├── HTTP Request Defaults           # base URL, headers comuns
├── Thread Group: Order Flow        # cenario principal
│   ├── HTTP Header Manager         # Content-Type, Auth
│   ├── CSV Data Set Config         # dados parametrizados
│   ├── Transaction Controller: List Orders
│   │   ├── HTTP Request: GET /api/v1/orders
│   │   ├── JSON Extractor: orderId
│   │   └── Response Assertion: status 200
│   ├── Transaction Controller: Create Order
│   │   ├── HTTP Request: POST /api/v1/orders
│   │   ├── JSON Extractor: newOrderId
│   │   └── Response Assertion: status 201
│   └── Gaussian Random Timer: 1000ms ± 500ms
└── Listeners
    ├── Summary Report              # metricas agregadas
    └── Backend Listener            # InfluxDB/Grafana
```

### Thread Groups

```
# Load test:    100 threads | Ramp: 2 min | Duration: 15 min
# Stress test:  500 threads | Ramp: 5 min | Duration: 10 min
# Spike test:   10 baseline → 300 spike (10s ramp) → 10 recovery
# Soak test:    50 threads  | Duration: 4 horas
```

### JDBC Sampler (testes de banco — exclusivo JMeter)

```xml
<JDBCSampler>
    <stringProp name="dataSource">orderDB</stringProp>
    <stringProp name="queryType">Select Statement</stringProp>
    <stringProp name="query">
        SELECT * FROM orders WHERE status = ? ORDER BY created_at DESC LIMIT 20
    </stringProp>
    <stringProp name="queryArguments">${STATUS}</stringProp>
    <stringProp name="queryArgumentsTypes">VARCHAR</stringProp>
</JDBCSampler>
```

### JMS Sampler (testes de messaging — exclusivo JMeter)

```xml
<PublisherSampler>
    <stringProp name="jms.provider_url">tcp://localhost:61616</stringProp>
    <stringProp name="jms.topic">orders.created</stringProp>
    <stringProp name="jms.text_message">
        {"orderId": "${ORDER_ID}", "status": "pending"}
    </stringProp>
</PublisherSampler>
```

### Extractors e Correlation

```xml
<!-- JSON Extractor — capturar valor para proximo request -->
<JSONPostProcessor>
    <stringProp name="JSONPostProcessor.referenceNames">orderId</stringProp>
    <stringProp name="JSONPostProcessor.jsonPathExprs">$.id</stringProp>
</JSONPostProcessor>
<!-- Uso: GET /api/v1/orders/${orderId} -->
```

### Funcoes uteis

```
${__Random(1,1000,)}           # numero aleatorio
${__UUID()}                    # UUID
${__time(yyyy-MM-dd,)}         # timestamp
${__counter(,)}                # contador incremental
${__P(ENV,default)}            # propriedade (CLI -J)
```

### Execucao headless (CLI)

```bash
jmeter -n -t test-plan.jmx \
    -l results.jtl \
    -e -o report/ \
    -JBASE_URL=http://api.example.com \
    -JTHREADS=100 \
    -JDURATION=900
```

### Regras JMeter

- **Nunca usar GUI para executar carga** — distorce resultados
- **Desabilitar View Results Tree em carga** — listener pesado
- **Transaction Controllers** — agrupar requests logicamente
- **CSV para dados** — nunca hardcoded
- **Think time entre requests** — simular usuario real

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
}
// Executar: java -jar benchmarks.jar -rf json -rff results.json
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
// Executar: go test -bench=. -benchmem -benchtime=5s ./...
```

## Locust (Python teams)

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

```bash
# Java — JFR
java -XX:StartFlightRecording=duration=60s,filename=recording.jfr -jar app.jar
# Java — async-profiler
java -agentpath:/path/to/libasyncProfiler.so=start,event=cpu,file=profile.html -jar app.jar
# Java — Heap dump
jmap -dump:format=b,file=heap.hprof <pid>
```

```go
// Go — pprof
import _ "net/http/pprof"
// CPU:  go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30
// Heap: go tool pprof http://localhost:6060/debug/pprof/heap
```

```bash
# Python — py-spy (sampling, sem overhead)
py-spy record -o profile.svg -- python app.py
```

## SLOs como thresholds

```javascript
// k6
export const options = {
  thresholds: {
    "checks": ["rate>0.999"],               // Availability: 99.9%
    "http_req_duration": ["p(95)<500"],      // Latency: p95 < 500ms
    "http_req_failed": ["rate<0.001"],       // Error: < 0.1%
    "http_reqs": ["rate>100"],              // Throughput: > 100 rps
  },
};
```

## Quando executar

| Momento | Tipo | Automatizado? |
|---------|------|--------------|
| PR com mudanca de performance | Benchmark (JMH/Go) | Sim (CI) |
| Pre-release | Load test (k6/Gatling/JMeter) | Sim (CD) |
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
- [ ] JMeter para protocolos nao-HTTP (JDBC, JMS) quando aplicavel?
