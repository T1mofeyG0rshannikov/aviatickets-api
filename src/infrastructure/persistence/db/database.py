from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.infrastructure.persistence.db.get_db_conf import get_db_config

SQLALCHEMY_DATABASE_URL = get_db_config().DATABASE_URL
SQLALCHEMY_SYNC_DATABASE_URL = get_db_config().SYNC_DATABASE_URL

engine = create_async_engine(SQLALCHEMY_DATABASE_URL, pool_size=15, max_overflow=50, pool_timeout=30)

sync_engine = create_engine(SQLALCHEMY_SYNC_DATABASE_URL)

new_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Session = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)


class Model(DeclarativeBase):
    pass


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def delete_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)


async def db_generator():
    async with new_session() as session:
        yield session


async def get_session():
    async for db in db_generator():
        yield db
