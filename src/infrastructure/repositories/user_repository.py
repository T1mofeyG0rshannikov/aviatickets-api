from sqlalchemy import select

from src.entities.user.dto import CreateUserDTO
from src.entities.user.user import User
from src.infrastructure.db.mappers.user import from_orm_to_user
from src.infrastructure.db.models.models import UserOrm
from src.infrastructure.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository):
    async def get(self, email: str = None, id: int = None) -> User:
        if email is not None:
            result = await self.db.execute(select(UserOrm).where(UserOrm.email == email))
        elif id is not None:
            result = await self.db.execute(select(UserOrm).where(UserOrm.id == id))
        else:
            return None

        user = result.scalar()
        return from_orm_to_user(user) if user else None

    async def create(self, data: CreateUserDTO) -> User:
        user = UserOrm(
            first_name=data.first_name,
            second_name=data.second_name,
            email=data.email,
            hash_password=data.hashed_password,
            is_superuser=data.is_superuser,
        )
        self.db.add(user)
        await self.db.commit()
        return from_orm_to_user(user)
