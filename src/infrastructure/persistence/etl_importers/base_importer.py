from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.persistence.persist_base import PersistBase

EntityType = TypeVar("EntityType")


class BaseOrmModel(Generic[EntityType]):
    @classmethod
    def from_entity(cls, obj: EntityType) -> "BaseOrmModel[EntityType]":  # type: ignore
        ...


OrmModel = TypeVar("OrmModel", bound=BaseOrmModel)


class BulkSaver(PersistBase, Generic[EntityType, OrmModel]):
    orm_model: type[OrmModel]

    def __init__(self, db: AsyncSession, orm_model: type[OrmModel]) -> None:
        self.orm_model = orm_model
        super().__init__(db)

    async def add_many(self, objects: list[EntityType]) -> None:
        orm_objects = [self.orm_model.from_entity(obj) for obj in objects]
        self.db.add_all(orm_objects)
