---
name: python-fastapi-patterns
description: "Padrões FastAPI: Pydantic v2, async, dependency injection, middleware, OpenAPI, background tasks. Use quando implementar APIs em FastAPI ou configurar projeto FastAPI."
---

# FastAPI — Patterns & Idioms

Padroes e idiomas para FastAPI em producao.

## Filosofia

- **Type hints como contrato**: Pydantic valida, FastAPI documenta — um so lugar
- **Async-first**: async/await para I/O, sync para CPU-bound
- **Dependency Injection**: funcoes como dependencias, composiveis e testaveis
- **OpenAPI automatico**: schema gerado a partir do codigo

## Estrutura de projeto

```
src/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app, startup/shutdown
│   ├── config.py            # Settings (pydantic-settings)
│   ├── dependencies.py      # Dependencias compartilhadas
│   ├── exceptions.py        # Exception handlers
│   ├── middleware.py         # Middlewares customizados
│   ├── features/
│   │   └── orders/
│   │       ├── __init__.py
│   │       ├── router.py    # Endpoints
│   │       ├── service.py   # Logica de negocio
│   │       ├── repository.py # Persistencia
│   │       ├── schemas.py   # Pydantic models (request/response)
│   │       ├── models.py    # SQLAlchemy/ORM models
│   │       └── dependencies.py # DI especifica da feature
│   └── core/
│       ├── database.py      # Engine, session
│       ├── security.py      # Auth, JWT
│       └── logging.py       # Structured logging
├── tests/
│   ├── conftest.py
│   └── features/orders/
├── pyproject.toml
└── Dockerfile
```

## App setup

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.features.orders.router import router as orders_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()

app = FastAPI(
    title="Order Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(orders_router, prefix="/api/v1/orders", tags=["orders"])
```

## Schemas (Pydantic v2)

```python
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class CreateOrderRequest(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    amount: float = Field(gt=0)
    description: str | None = Field(default=None, max_length=500)

class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    amount: float
    status: str
    created_at: datetime

class PaginatedResponse[T](BaseModel):
    items: list[T]
    total: int
    page: int
    size: int
    pages: int
```

## Router (endpoints)

```python
from fastapi import APIRouter, Depends, HTTPException, Query, status

router = APIRouter()

@router.get("", response_model=PaginatedResponse[OrderResponse])
async def list_orders(
    status_filter: str | None = Query(None, alias="status"),
    page: int = Query(0, ge=0),
    size: int = Query(20, ge=1, le=100),
    service: OrderService = Depends(get_order_service),
):
    return await service.list(status=status_filter, page=page, size=size)

@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    request: CreateOrderRequest,
    service: OrderService = Depends(get_order_service),
):
    return await service.create(request)

@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: str,
    service: OrderService = Depends(get_order_service),
):
    order = await service.find_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
```

## Dependency Injection

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session

def get_order_repository(db: AsyncSession = Depends(get_db)) -> OrderRepository:
    return OrderRepository(db)

def get_order_service(
    repo: OrderRepository = Depends(get_order_repository),
    payment_client: PaymentClient = Depends(get_payment_client),
) -> OrderService:
    return OrderService(repo, payment_client)
```

## Exception Handlers

```python
from fastapi import Request
from fastapi.responses import JSONResponse

class DomainError(Exception):
    def __init__(self, type_: str, detail: str, status_code: int = 422):
        self.type = type_
        self.detail = detail
        self.status_code = status_code

@app.exception_handler(DomainError)
async def domain_error_handler(request: Request, exc: DomainError) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"type": exc.type, "detail": exc.detail},
    )

@app.exception_handler(Exception)
async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("unhandled_error", error=str(exc), path=request.url.path)
    return JSONResponse(
        status_code=500,
        content={"type": "internal_error", "detail": "Internal server error"},
    )
```

## Middleware

```python
import time
import uuid
import structlog
from starlette.middleware.base import BaseHTTPMiddleware

class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        structlog.contextvars.bind_contextvars(request_id=request_id)

        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000

        logger.info(
            "request",
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            duration_ms=round(duration_ms, 2),
        )

        response.headers["X-Request-ID"] = request_id
        return response

app.add_middleware(RequestContextMiddleware)
```

## Configuration (pydantic-settings)

```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "order-service"
    debug: bool = False
    database_url: str
    redis_url: str | None = None
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
    cors_origins: list[str] = ["http://localhost:3000"]

settings = Settings()
```

## Auth (JWT)

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    try:
        payload = jwt.decode(credentials.credentials, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return await user_service.find_by_id(user_id)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Uso
@router.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    return user
```

## Background Tasks

```python
from fastapi import BackgroundTasks

@router.post("/{order_id}/confirm")
async def confirm_order(
    order_id: str,
    background_tasks: BackgroundTasks,
    service: OrderService = Depends(get_order_service),
):
    order = await service.confirm(order_id)
    background_tasks.add_task(send_confirmation_email, order.email, order.id)
    return order
```

## SQLAlchemy Async

```python
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine(settings.database_url, pool_size=10, max_overflow=20)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

class Order(Base):
    __tablename__ = "orders"
    id: Mapped[str] = mapped_column(primary_key=True)
    title: Mapped[str]
    amount: Mapped[float]
    status: Mapped[str] = mapped_column(default="pending")
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_by_id(self, id: str) -> Order | None:
        return await self.session.get(Order, id)

    async def list(self, status: str | None, page: int, size: int) -> list[Order]:
        query = select(Order).order_by(Order.created_at.desc())
        if status:
            query = query.where(Order.status == status)
        query = query.offset(page * size).limit(size)
        result = await self.session.execute(query)
        return list(result.scalars().all())
```

## Testing

```python
import pytest
from httpx import AsyncClient, ASGITransport

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.mark.anyio
async def test_create_order(client: AsyncClient):
    response = await client.post("/api/v1/orders", json={"title": "Test", "amount": 99.90})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test"
    assert data["status"] == "pending"

@pytest.mark.anyio
async def test_create_order_validation(client: AsyncClient):
    response = await client.post("/api/v1/orders", json={"title": "", "amount": -1})
    assert response.status_code == 422

# Dependency override
@pytest.fixture
def mock_service():
    service = AsyncMock(spec=OrderService)
    service.list.return_value = PaginatedResponse(items=[], total=0, page=0, size=20, pages=0)
    app.dependency_overrides[get_order_service] = lambda: service
    yield service
    app.dependency_overrides.clear()
```

## Checklist

- [ ] Pydantic v2 para schemas (request/response)?
- [ ] Dependency injection para services e repositories?
- [ ] Exception handlers para erros de dominio?
- [ ] Middleware de request ID e structured logging?
- [ ] pydantic-settings para configuracao (env vars)?
- [ ] Lifespan events para startup/shutdown?
- [ ] Auth com HTTPBearer + JWT?
- [ ] SQLAlchemy async para persistencia?
- [ ] Testes com httpx AsyncClient + dependency override?
- [ ] Health endpoint (/health)?
- [ ] OpenAPI schema gerado automaticamente?
