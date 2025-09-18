from sqlalchemy.ext.asyncio import AsyncSession


class PersistenceBase:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
