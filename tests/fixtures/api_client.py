import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.infrastructure.persistence.db.database import db_generator
from src.main import app


@pytest.fixture
def client():
    print(app.dependency_overrides)
    SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:root@localhost:5432/test_aero"
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL, pool_size=15, max_overflow=50, pool_timeout=30)
    new_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async def test_db_generator():
        async with new_session() as session:
            yield session

    app.dependency_overrides[db_generator] = test_db_generator

    with TestClient(app=app) as c:
        yield c
