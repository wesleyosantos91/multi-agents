# Python Testing — pytest Patterns

Guia de testes com pytest para projetos Python.

## Fixtures

### conftest.py (fixtures globais)
```python
import pytest
from httpx import AsyncClient, ASGITransport
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope="session")
def postgres():
    """Real PostgreSQL via Testcontainers."""
    with PostgresContainer("postgres:16-alpine") as pg:
        yield pg


@pytest.fixture
def db_session(postgres):
    """Database session com rollback automático."""
    engine = create_engine(postgres.get_connection_url())
    Base.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.rollback()
    session.close()


@pytest.fixture
def order_repo(db_session):
    return PostgresOrderRepository(db_session)


@pytest.fixture
def order_service(order_repo):
    return OrderService(order_repo)


@pytest.fixture
async def client(order_service):
    """Test client para FastAPI."""
    app.dependency_overrides[get_order_service] = lambda: order_service
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        yield ac
    app.dependency_overrides.clear()
```

## Parametrize
```python
@pytest.mark.parametrize("status,cancellable", [
    (OrderStatus.PENDING, True),
    (OrderStatus.CONFIRMED, True),
    (OrderStatus.SHIPPED, False),
    (OrderStatus.DELIVERED, False),
    (OrderStatus.CANCELLED, False),
])
def test_order_cancellable(status: OrderStatus, cancellable: bool):
    order = Order(id="1", status=status, items=[], customer_id="c1", total=Decimal("0"))
    assert order.is_cancellable() == cancellable


@pytest.mark.parametrize("amount,tier,expected", [
    (Decimal("100"), "standard", Decimal("100")),
    (Decimal("100"), "premium", Decimal("90")),
    (Decimal("100"), "vip", Decimal("80")),
], ids=["standard-no-discount", "premium-10%-off", "vip-20%-off"])
def test_calculate_discount(amount, tier, expected):
    assert calculate_discount(amount, tier) == expected
```

## Testes assíncronos
```python
@pytest.mark.asyncio
async def test_create_order(client: AsyncClient, order_service):
    response = await client.post("/api/v1/orders", json={
        "customer_id": "cust-1",
        "items": [{"product_id": "prod-1", "quantity": 2, "price": "50.00"}],
    })
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "PENDING"
    assert data["id"] is not None


@pytest.mark.asyncio
async def test_get_order_not_found(client: AsyncClient):
    response = await client.get("/api/v1/orders/nonexistent")
    assert response.status_code == 404
```

## Mocking
```python
from unittest.mock import AsyncMock, patch


@pytest.fixture
def mock_payment_client():
    client = AsyncMock()
    client.charge.return_value = PaymentResult(
        transaction_id="txn-123", status="approved"
    )
    return client


async def test_process_payment_success(mock_payment_client):
    svc = PaymentService(client=mock_payment_client)
    result = await svc.process(PaymentRequest(amount=Decimal("100"), order_id="ord-1"))
    assert result.status == "approved"
    mock_payment_client.charge.assert_called_once()


# Patch para dependências externas
@patch("myservice.infrastructure.clients.httpx.AsyncClient.post")
async def test_external_service_timeout(mock_post):
    mock_post.side_effect = httpx.TimeoutException("timeout")
    with pytest.raises(ExternalServiceUnavailable):
        await external_client.call_service(request)
```

## Testes de exceção
```python
def test_cancel_shipped_order_raises():
    order = OrderFixture.shipped()
    with pytest.raises(OrderNotCancellableError, match="shipped"):
        order.cancel()


def test_create_order_empty_items_raises():
    with pytest.raises(ValidationError) as exc_info:
        Order.create(customer_id="c1", items=[])
    assert "items" in str(exc_info.value)
```

## Testes de integração com Testcontainers
```python
@pytest.mark.integration
class TestOrderRepositoryIntegration:

    def test_save_and_find(self, order_repo, db_session):
        order = OrderFixture.pending()
        saved = order_repo.save(order)

        found = order_repo.find_by_id(saved.id)
        assert found is not None
        assert found.customer_id == order.customer_id
        assert found.status == OrderStatus.PENDING

    def test_find_nonexistent_returns_none(self, order_repo):
        assert order_repo.find_by_id("nonexistent") is None

    def test_list_by_status(self, order_repo):
        order_repo.save(OrderFixture.pending())
        order_repo.save(OrderFixture.pending())
        order_repo.save(OrderFixture.shipped())

        pending = order_repo.list_by_status(OrderStatus.PENDING)
        assert len(pending) == 2
```

## Fixtures Pattern
```python
class OrderFixture:
    @staticmethod
    def pending(**overrides) -> Order:
        defaults = {
            "id": str(uuid4()),
            "customer_id": "cust-1",
            "status": OrderStatus.PENDING,
            "items": [OrderItem(product_id="prod-1", quantity=1, price=Decimal("50"))],
            "total": Decimal("50"),
            "created_at": datetime.now(UTC),
        }
        defaults.update(overrides)
        return Order(**defaults)

    @staticmethod
    def shipped(**overrides) -> Order:
        return OrderFixture.pending(status=OrderStatus.SHIPPED, **overrides)
```

## Testes de Lambda handler
```python
def test_lambda_handler_success():
    event = {
        "Records": [{
            "body": json.dumps({"order_id": "ord-1", "action": "process"}),
            "messageId": "msg-1",
        }]
    }
    result = handler(event, None)
    assert result["batchItemFailures"] == []


def test_lambda_handler_malformed_payload():
    event = {"Records": [{"body": "not json", "messageId": "msg-1"}]}
    result = handler(event, None)
    assert len(result["batchItemFailures"]) == 1
```

## Comandos
```bash
pytest                              # rodar todos
pytest -x                           # parar no primeiro erro
pytest -k "test_create"             # filtrar por nome
pytest -m "not integration"         # pular integração
pytest --cov=src --cov-report=html  # cobertura com relatório
pytest -v tests/unit/               # verbose em um diretório
pytest --tb=short                   # traceback curto
```

## Checklist
- [ ] conftest.py com fixtures reutilizáveis?
- [ ] parametrize para casos múltiplos?
- [ ] Testcontainers para banco real em integração?
- [ ] Markers para separar unit/integration?
- [ ] AsyncMock para dependências assíncronas?
- [ ] Fixtures pattern para criar objetos de teste?
- [ ] Cobertura medida (`--cov`)?
- [ ] Testes de exceção com `pytest.raises`?
