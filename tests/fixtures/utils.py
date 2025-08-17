import json
from datetime import datetime
from typing import Type, TypeVar

from sqlalchemy import TIMESTAMP, Boolean, Integer, Numeric
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.db.database import Model

T = TypeVar("T", bound=Model)


class OrmJsonLoader:
    def orm_obj_from_json(self, model: type[T], data: dict) -> T:
        for field_name, field_value in data.items():
            column = getattr(model, field_name).property.columns[0]
            if isinstance(column.type, (Integer, Numeric)):
                data[field_name] = int(field_value) if field_value != "None" else None
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
