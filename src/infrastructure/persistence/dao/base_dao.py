from sqlalchemy.ext.asyncio import AsyncSession


class BaseDAO:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
