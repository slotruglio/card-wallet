import pytest
import asyncio
from httpx import AsyncClient
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.model.base import BaseORM
from app.model.user import UserORM
from app.model.gift_card import GiftCardORM
import uuid

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Async engine & session
engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Event loop for pytest-asyncio
@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()

# Initialize tables once per test session
@pytest.fixture(scope="session", autouse=True)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(BaseORM.metadata.create_all)
    yield
    await engine.dispose()

# Provide session per test
@pytest.fixture()
async def db_session():
    async with AsyncSessionLocal() as session:
        yield session

# Test client with overridden session
@pytest.fixture()
async def client(db_session):
    from app.utility.db import get_session
    app.dependency_overrides[get_session] = lambda: db_session
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c

# Fixture: sample user
@pytest.fixture()
async def sample_user(db_session):
    user = UserORM(name="John Doe")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

# Fixture: sample giftcard
@pytest.fixture()
async def sample_giftcard(db_session, sample_user):
    gc = GiftCardORM(
        id=uuid.uuid4(),
        supplier="Amazon",
        amount=10000,
        spent_amount=0,
        user_id=sample_user.id
    )
    db_session.add(gc)
    await db_session.commit()
    await db_session.refresh(gc)
    return gc
