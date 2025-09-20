import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from avia.infrastructure.persistence.db.database import db_generator
from avia.infrastructure.persistence.db.get_db_conf import get_db_config
from avia.main import app


@pytest.fixture
def client():
    print(app.dependency_overrides)
    SQLALCHEMY_DATABASE_URL = get_db_config().DATABASE_URL
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL, pool_size=15, max_overflow=50, pool_timeout=30)
    new_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async def test_db_generator():
        async with new_session() as session:
            yield session

    app.dependency_overrides[db_generator] = test_db_generator

    with TestClient(app=app) as c:
        yield c
