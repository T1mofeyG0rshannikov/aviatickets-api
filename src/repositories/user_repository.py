from sqlalchemy import select

from src.db.mappers.user import from_orm_to_user
from src.db.models.models import UserOrm
from src.entities.user import User
from src.repositories.base_reposiotory import BaseRepository


class UserRepository(BaseRepository):
    async def get(self, email: str) -> User:
        result = await self.db.execute(select(UserOrm).where(UserOrm.email == email))
        user = result.scalar()
        return from_orm_to_user(user)

    async def create(self, username: str, email: str, hashed_password: str, is_superuser: bool = False) -> User:
        user = UserOrm(username=username, email=email, hash_password=hashed_password, is_superuser=is_superuser)
        self.db.add(user)
        await self.db.commit()
        return from_orm_to_user(user)
