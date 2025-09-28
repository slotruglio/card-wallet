import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Get DB connection URL from env
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://fastapi:fastapi@localhost:5432/fastapi_db")

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=False, future=True)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

# Dependency for FastAPI routes
async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.close()
