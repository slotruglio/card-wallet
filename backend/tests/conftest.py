# conftest.py
from typing import AsyncGenerator
import uuid
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncConnection

from app.main import app  # your FastAPI app
from app.model.base import BaseORM
from app.model.user import UserORM
from app.model.gift_card import GiftCardORM
from app.utility.db import DATABASE_URL, get_session

CLIENT_BASE_URL = "http://test"

# To run async tests
pytestmark = pytest.mark.anyio

engine = create_async_engine(DATABASE_URL)
# Required per https://anyio.readthedocs.io/en/stable/testing.html#using-async-fixtures-with-higher-scopes
@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def connection(anyio_backend) -> AsyncGenerator[AsyncConnection, None]:
    async with engine.connect() as connection:
        yield connection

        
@pytest.fixture()
async def transaction(
    connection: AsyncConnection,
) -> AsyncGenerator:
    async with connection.begin() as transaction:
        yield transaction


# Use this fixture to get SQLAlchemy's AsyncSession.
# All changes that occur in a test function are rolled back
# after function exits, even if session.commit() is called
# in inner functions
@pytest.fixture()
async def session(
    connection, transaction
) -> AsyncGenerator[AsyncSession, None]:
    async_session = AsyncSession(
        bind=connection,
        join_transaction_mode="create_savepoint",
        expire_on_commit=False
    )

    yield async_session

    await transaction.rollback()

# Use this fixture to get HTTPX's client to test API.
# All changes that occur in a test function are rolled back
# after function exits, even if session.commit() is called
# in FastAPI's application endpoints
@pytest.fixture()
async def client(
    connection, transaction
) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
        async_session = AsyncSession(
            bind=connection,
            join_transaction_mode="create_savepoint",
        )
        async with async_session:
            yield async_session
    
    # Here you have to override the dependency that is used in FastAPI's
    # endpoints to get SQLAlchemy's AsyncSession. In my case, it is
    # get_async_session
    app.dependency_overrides[get_session] = override_get_async_session
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url=CLIENT_BASE_URL,
        follow_redirects=True
    ) as ac:
        yield ac
        
    del app.dependency_overrides[get_session]

    await transaction.rollback()

# Sample user
@pytest.fixture()
async def sample_user(session):
    async with session.begin():
        user = UserORM(name="John Doe")
        session.add(user)
        await session.flush()
        await session.refresh(user)
        return user

# Sample giftcard
@pytest.fixture()
async def sample_giftcard(session, sample_user):
    async with session.begin():
        gc = GiftCardORM(
            id=uuid.uuid4(),
            supplier="Amazon",
            amount=10000,
            spent_amount=0,
            user_id=sample_user.id,
        )
        session.add(gc)
        await session.flush()
        await session.refresh(gc)
        return gc
