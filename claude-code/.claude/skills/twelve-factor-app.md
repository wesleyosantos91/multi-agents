---
name: twelve-factor-app
description: "12-Factor App e princípios cloud-native: config via env, stateless, logs as streams, dev/prod parity. Use quando projetar serviços cloud-native ou avaliar aderência a boas práticas."
---

# 12-Factor App — Cloud-Native Principles

Os 12 fatores para aplicacoes cloud-native resilientes e operaveis.

## Os 12 Fatores

### I. Codebase — Um codebase, multiplos deploys

```
Um repo → multiple deploys (dev, staging, prod)
NAO: repos separados por ambiente
NAO: codigo compartilhado via copy-paste entre repos
SIM: um repo, branches/tags, config por ambiente
```

### II. Dependencies — Declarar e isolar

```xml
<!-- Java: pom.xml com versoes explicitas -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
    <!-- versao herdada do parent, nao implicita -->
</dependency>
```

```toml
# Python: pyproject.toml com ranges
[project]
dependencies = [
    "fastapi>=0.111,<1.0",
    "sqlalchemy>=2.0,<3.0",
]
```

```go
// Go: go.mod com versoes exatas
require (
    github.com/gin-gonic/gin v1.10.0
    github.com/jackc/pgx/v5 v5.7.0
)
```

**Regra**: nunca depender de pacotes do sistema. Tudo declarado e isolado (Docker, venv, go modules).

### III. Config — Config via ambiente

```yaml
# SIM: variavel de ambiente
spring:
  datasource:
    url: ${DATABASE_URL}

# NAO: hardcoded
spring:
  datasource:
    url: jdbc:postgresql://prod-db:5432/orders
```

```python
# SIM: pydantic-settings le de env automaticamente
class Settings(BaseSettings):
    database_url: str        # DATABASE_URL
    redis_url: str | None    # REDIS_URL
    debug: bool = False      # DEBUG
```

**Teste**: o codebase poderia ser open source agora sem vazar credenciais?

### IV. Backing Services — Tratar como recursos anexados

```
Database, cache, fila, email, storage → todos sao "attached resources"
Trocar de Postgres local para RDS → so mudar a URL, sem mudar codigo

# Dev
DATABASE_URL=postgresql://localhost:5432/orders
CACHE_URL=redis://localhost:6379

# Prod
DATABASE_URL=postgresql://rds-instance.amazonaws.com:5432/orders
CACHE_URL=redis://elasticache.amazonaws.com:6379
```

### V. Build, Release, Run — Separar build de run

```
Build  → compila codigo, gera artefato (JAR, Docker image, zip)
Release → artefato + config do ambiente = release imutavel
Run    → executa a release no ambiente

# CI/CD
build:    mvn package -DskipTests=false → app.jar
release:  docker build → image:v1.2.3 + env vars do ambiente
run:      docker run image:v1.2.3 (ou Lambda deploy)
```

**Regra**: releases sao imutaveis e versionadas. Nunca editar codigo em runtime.

### VI. Processes — Stateless e share-nothing

```java
// SIM: stateless — estado no backing service
@RestController
public class OrderController {
    @GetMapping("/orders/{id}")
    public Order getOrder(@PathVariable String id) {
        return repository.findById(id); // estado no DB
    }
}

// NAO: estado em memoria
private final Map<String, Order> cache = new HashMap<>(); // morre no restart
```

**Regra**: sessoes em Redis/DynamoDB, nao em memoria. Cada processo e descartavel.

### VII. Port Binding — Exportar servico via porta

```dockerfile
# A app e self-contained — exporta HTTP na porta
EXPOSE 8080
CMD ["java", "-jar", "app.jar"]

# NAO depende de servidor externo (Tomcat instalado no host)
# SIM: servidor embarcado (Spring Boot, Uvicorn, Go net/http)
```

### VIII. Concurrency — Escalar via processos

```
NAO: um processo gigante com muitas threads
SIM: multiplos processos independentes

# Horizontal scaling
web:     3 instancias (HTTP requests)
worker:  2 instancias (SQS consumer)
cron:    1 instancia  (jobs agendados)

# Lambda: concorrencia = numero de invocacoes simultaneas
# ECS: concorrencia = numero de tasks
```

### IX. Disposability — Startup rapido, shutdown graceful

```java
// Graceful shutdown — Spring Boot
@PreDestroy
public void shutdown() {
    // Completar requests em andamento
    // Fechar conexoes
    // Commitar offsets Kafka
}
```

```go
// Go — signal handling
quit := make(chan os.Signal, 1)
signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
<-quit

ctx, cancel := context.WithTimeout(context.Background(), 15*time.Second)
defer cancel()
srv.Shutdown(ctx)
```

**Regra**: startup em segundos (nao minutos). Shutdown completa trabalho em andamento.

### X. Dev/Prod Parity — Minimizar gaps

| Gap | Problema | Solucao |
|-----|----------|---------|
| **Tempo** | Deploy semanal | Deploy continuo (diario ou mais) |
| **Pessoal** | Dev escreve, Ops deploya | DevOps — quem escreve, deploya |
| **Ferramentas** | SQLite local, Postgres prod | Mesmo stack local (Docker, Ministack) |

```yaml
# docker-compose.yml — mesmo stack local e producao
services:
  postgres:
    image: postgres:16
  redis:
    image: redis:7
  ministack:
    image: ministack/ministack:latest
    ports: ["4566:4566"]
```

### XI. Logs — Tratar como streams de eventos

```java
// SIM: stdout/stderr — plataforma coleta
logger.info("order_created", Map.of("orderId", order.getId(), "amount", order.getAmount()));

// NAO: escrever em arquivo
FileWriter fw = new FileWriter("/var/log/app.log"); // anti-pattern
```

```python
# SIM: structlog → stdout
import structlog
logger = structlog.get_logger()
logger.info("order_created", order_id=order.id, amount=order.amount)
```

```go
// SIM: slog → stdout
slog.Info("order_created", "orderId", order.ID, "amount", order.Amount)
```

**Regra**: app escreve em stdout. CloudWatch/Datadog/ELK coleta.

### XII. Admin Processes — Executar como one-off

```bash
# Migrations como processo separado
java -jar app.jar --spring.main.web-application-type=none db-migrate

# Django
python manage.py migrate

# Go
go run cmd/migrate/main.go

# NAO: rodar migration no startup da app
# SIM: migration como step separado no pipeline de deploy
```

## Beyond 12-Factor (extras modernos)

| Fator | Principio |
|-------|-----------|
| **API-first** | Contrato antes de implementacao |
| **Telemetry** | Metricas, traces, logs desde o dia 1 |
| **Auth/AuthZ** | Seguranca como requisito, nao afterthought |
| **Ephemeral infrastructure** | Infra descartavel, recriavel (IaC) |

## Checklist de aderencia

- [ ] Um codebase → multiplos deploys?
- [ ] Dependencias declaradas e isoladas (sem deps do sistema)?
- [ ] Config 100% via environment variables (zero hardcoded)?
- [ ] Backing services tratados como recursos anexados?
- [ ] Build → Release → Run separados e imutaveis?
- [ ] Processos stateless e share-nothing?
- [ ] Servico exportado via port binding (servidor embarcado)?
- [ ] Escalavel horizontalmente via processos?
- [ ] Startup rapido (< 10s) e graceful shutdown?
- [ ] Dev/prod parity (mesmo stack, Docker Compose)?
- [ ] Logs em stdout como streams de eventos?
- [ ] Admin tasks como processos one-off separados?
