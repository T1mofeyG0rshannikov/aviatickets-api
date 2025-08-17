import json

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.infrastructure.db.database import Model, delete_tables
from src.infrastructure.db.models.models import (
    AirlineOrm,
    AirportOrm,
    CityOrm,
    CountryOrm,
    RegionOrm,
    TicketOrm,
    UserOrm,
)

from .utils import OrmJsonLoader


@pytest.fixture
def engine():
    SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:root@localhost:5432/test_aero"
    return create_async_engine(SQLALCHEMY_DATABASE_URL, pool_size=15, max_overflow=50, pool_timeout=30)


async def create_tables(engine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables(engine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)


@pytest.fixture
async def db(engine):
    new_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with new_session() as session:
        yield session


@pytest.fixture
def orm_json_loader() -> OrmJsonLoader:
    return OrmJsonLoader()


@pytest.fixture
async def populate_db(engine, db, orm_json_loader: OrmJsonLoader):
    await delete_tables(engine)
    await create_tables(engine)
    await orm_json_loader.load_objects(CountryOrm, db, "tests/data/countries.json")
    await orm_json_loader.load_objects(CityOrm, db, "tests/data/cities.json")
    await orm_json_loader.load_objects(RegionOrm, db, "tests/data/regions.json")
    await orm_json_loader.load_objects(AirlineOrm, db, "tests/data/airlines.json")
    await orm_json_loader.load_objects(AirportOrm, db, "tests/data/airports.json")
    await orm_json_loader.load_objects(TicketOrm, db, "tests/data/tickets.json")
    await orm_json_loader.load_objects(UserOrm, db, "tests/data/users.json")
