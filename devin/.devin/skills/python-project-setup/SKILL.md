---
name: python-project-setup
description: "Estrutura e setup de projetos Python modernos com pyproject.toml, src layout, pytest e Ruff. Use quando criar projeto Python, configurar ambiente, ou revisar estrutura Python."
argument-hint: "[contexto adicional]"
---

# Python Project Setup — Modern Best Practices

Guia para estruturar projetos Python modernos (3.12+).

## Estrutura de projeto

### API / Serviço
```
myservice/
├── src/
│   └── myservice/
│       ├── __init__.py
│       ├── main.py              # Entrypoint (FastAPI/Flask app)
│       ├���─ config.py            # Configuração via pydantic-settings
│       ├���─ domain/
│       │   ├── __init__.py
│       │   ├── model.py         # Entidades, dataclasses, Pydantic models
│       │   ├── service.py       # Lógica de negócio
│       │   ├── repository.py    # Interfaces (Protocol)
│       │   └── exceptions.py    # Exceções de domínio
���       ├── api/
│       │   ��── __init__.py
│       │   ├── router.py        # Routes/endpoints
│       │   ├── schemas.py       # Request/Response models
│       │   └── dependencies.py  # DI via Depends
│       ├── infrastructure/
│       │   ├── __init__.py
│       │   ├── database.py      # SQLAlchemy / DynamoDB setup
│       │   ├── repository.py    # Implementação de persistência
��       │   └── clients.py       # Clientes HTTP externos
│       └── message/
│           ├── __init__.py
│           ��── consumer.py      # SQS/Kafka consumers
│           └── producer.py      # SQS/Kafka producers
├── tests/
│   ├── conftest.py              # Fixtures globais
│   ���── unit/
│   │   └── test_service.py
│   ├── integration/
│   │   └── test_repository.py
│   └��─ api/
│       └── test_orders.py
├── pyproject.toml               # Build, deps, tools — tudo aqui
├── Makefile
├── Dockerfile
└── README.md
```

### Lambda function
```
lambda-python/
├── src/
│   └── handler/
│       ├── __init__.py
│       ├─�� main.py              # Lambda handler (fino)
│       ├── domain/              # Lógica testável sem AWS
│       └── adapter/             # DynamoDB, SQS, etc
├── tests/
├── pyproject.toml
└── Dockerfile
```

## pyproject.toml completo
```toml
[project]
name = "myservice"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.115",
    "uvicorn[standard]>=0.32",
    "pydantic>=2.9",
    "pydantic-settings>=2.6",
    "sqlalchemy>=2.0",
    "httpx>=0.27",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3",
    "pytest-asyncio>=0.24",
    "pytest-cov>=5.0",
    "httpx>=0.27",  # TestClient
    "testcontainers[postgres]>=4.8",
    "ruff>=0.7",
    "mypy>=1.13",
]

[tool.ruff]
target-version = "py312"
line-length = 120

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "SIM", "S", "A", "C4", "RUF"]
ignore = ["S101"]  # assert em testes

[tool.ruff.lint.isort]
known-first-party = ["myservice"]

[tool.pytest.ini_options]
testpaths = ["tests"]
asyncio_mode = "auto"
addopts = "-ra --strict-markers"
markers = [
    "integration: marks tests as integration (deselect with '-m \"not integration\"')",
]

[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
```

## Type hints (obrigatório)
```python
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime


@dataclass(frozen=True)
class Order:
    id: str
    customer_id: str
    items: list["OrderItem"]
    status: "OrderStatus"
    total: Decimal
    created_at: datetime


# Protocol para interfaces (dependency inversion)
from typing import Protocol

class OrderRepository(Protocol):
    async def find_by_id(self, order_id: str) -> Order | None: ...
    async def save(self, order: Order) -> Order: ...
```

## Configuration (pydantic-settings)
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    port: int = 8080
    log_level: str = "INFO"
    aws_region: str = "sa-east-1"
    sqs_queue_url: str | None = None

    model_config = {"env_prefix": "APP_"}

settings = Settings()
```

## FastAPI patterns
```python
from fastapi import FastAPI, Depends, HTTPException, status

app = FastAPI(title="Order Service")

# Dependency injection
async def get_order_service() -> OrderService:
    repo = PostgresOrderRepository(get_db())
    return OrderService(repo)

@app.post("/api/v1/orders", status_code=status.HTTP_201_CREATED)
async def create_order(
    request: CreateOrderRequest,
    service: OrderService = Depends(get_order_service),
) -> OrderResponse:
    order = await service.create(request.to_domain())
    return OrderResponse.from_domain(order)

# Exception handler global
@app.exception_handler(DomainError)
async def domain_error_handler(request, exc: DomainError):
    return JSONResponse(
        status_code=422,
        content={"type": exc.error_type, "detail": str(exc)},
    )
```

## Logging estruturado
```python
import logging
import structlog

structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer(),
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    logger_factory=structlog.stdlib.LoggerFactory(),
)

logger = structlog.get_logger()
logger.info("order_created", order_id=order.id, customer_id=order.customer_id)
```

## Makefile
```makefile
.PHONY: install test lint format run

install:
	pip install -e ".[dev]"

test:
	pytest --cov=src --cov-report=term-missing

test-unit:
	pytest -m "not integration" --cov=src

lint:
	ruff check src tests
	mypy src

format:
	ruff format src tests
	ruff check --fix src tests

run:
	uvicorn src.myservice.main:app --reload --port 8080
```

## Checklist
- [ ] `src/` layout com `pyproject.toml`?
- [ ] Type hints em todo código de produção?
- [ ] Protocol para interfaces (dependency inversion)?
- [ ] pydantic-settings para configuração?
- [ ] Ruff configurado (lint + format)?
- [ ] mypy strict habilitado?
- [ ] pytest com fixtures e markers?
- [ ] structlog para logging JSON?
- [ ] Makefile com targets: install, test, lint, format, run?
