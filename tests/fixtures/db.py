import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from avia.infrastructure.persistence.db.database import Model
from avia.infrastructure.persistence.db.get_db_conf import get_db_config
from avia.infrastructure.persistence.db.models.models import (
    AircraftOrm,
    AirlineOrm,
    AirportOrm,
    CityOrm,
    CountryOrm,
    RegionOrm,
    TicketItineraryOrm,
    TicketOrm,
    TicketSegmentOrm,
    UserOrm,
)

from .utils import OrmJsonLoader


@pytest.fixture
def engine():
    SQLALCHEMY_DATABASE_URL = get_db_config().DATABASE_URL
    print(SQLALCHEMY_DATABASE_URL)
    return create_async_engine(SQLALCHEMY_DATABASE_URL, pool_size=15, max_overflow=50, pool_timeout=30)


async def create_tables(engine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables(engine) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)


@pytest.fixture
async def db(engine):
    await delete_tables(engine)
    await create_tables(engine)
    new_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    async with new_session() as session:
        yield session


@pytest.fixture
async def transaction(engine):
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
    await orm_json_loader.load_objects(CountryOrm, db, "data/countries.json")
    await orm_json_loader.load_objects(CityOrm, db, "data/cities.json")
    await orm_json_loader.load_objects(RegionOrm, db, "data/regions.json")
    await orm_json_loader.load_objects(AirlineOrm, db, "data/airlines.json")
    await orm_json_loader.load_objects(AircraftOrm, db, "data/aircrafts.json")
    await orm_json_loader.load_objects(AirportOrm, db, "data/airports.json")
    await orm_json_loader.load_objects(TicketOrm, db, "data/tickets.json")
    await orm_json_loader.load_objects(TicketItineraryOrm, db, "data/ticket_itineraries.json")
    await orm_json_loader.load_objects(TicketSegmentOrm, db, "data/ticket_segments.json")
    await orm_json_loader.load_objects(UserOrm, db, "data/users.json")


@pytest.fixture
async def populate_cities_db(engine, db, orm_json_loader: OrmJsonLoader):
    await create_tables(engine)
    await orm_json_loader.load_objects(CityOrm, db, "data/cities.json")


@pytest.fixture
async def populate_countries_db(engine, db, orm_json_loader: OrmJsonLoader):
    await create_tables(engine)
    await orm_json_loader.load_objects(CountryOrm, db, "data/countries.json")


@pytest.fixture
async def populate_regions_db(engine, db, orm_json_loader: OrmJsonLoader):
    await create_tables(engine)
    await orm_json_loader.load_objects(RegionOrm, db, "data/regions.json")
