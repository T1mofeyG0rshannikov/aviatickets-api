import json
from datetime import datetime
from typing import Type, TypeVar
from uuid import UUID

from sqlalchemy import TIMESTAMP
from sqlalchemy import UUID as DbUUID
from sqlalchemy import Boolean, Float, Integer
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.persistence.db.database import Model

T = TypeVar("T", bound=Model)


class OrmJsonLoader:
    def orm_obj_from_json(self, model: type[T], data: dict) -> T:
        for field_name, field_value in data.items():
            column = getattr(model, field_name).property.columns[0]

            if field_value == "None":
                data[field_name] = None
            if isinstance(column.type, DbUUID):
                data[field_name] = UUID(field_value) if field_value != "None" else None
            if isinstance(column.type, Integer):
                data[field_name] = int(field_value) if field_value != "None" else None
            if isinstance(column.type, Float):
                data[field_name] = float(field_value) if field_value != "None" else None
            elif isinstance(column.type, TIMESTAMP):
                data[field_name] = datetime.fromisoformat(field_value)
            elif isinstance(column.type, Boolean):
                data[field_name] = field_value == "True"

        return model(**data)

    async def load_objects(self, model: type[T], session: AsyncSession, json_path: str) -> None:
        with open(json_path, encoding="utf-8") as file:
            test_objects = []
            data = json.load(file)

            for obj_data in data:
                test_objects.append(self.orm_obj_from_json(model, obj_data))

            session.add_all(test_objects)
            await session.commit()
