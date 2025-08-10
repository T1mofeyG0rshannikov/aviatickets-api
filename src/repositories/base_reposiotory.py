from typing import TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import Model

T = TypeVar("T", bound=Model)


class BaseRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def update(self, obj: T) -> T:
        await self.db.commit()
        await self.db.refresh(obj)
        return obj
