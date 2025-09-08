from sqlalchemy.ext.asyncio import AsyncSession


class PersistBase:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
