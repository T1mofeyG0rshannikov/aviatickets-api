from sqlalchemy import select

from src.entities.user.user import User
from src.entities.user.user_repository import UserRepositoryInterface
from src.entities.user.value_objects.email import Email
from src.entities.value_objects.entity_id import EntityId
from src.infrastructure.persistence.db.models.models import UserOrm
from src.infrastructure.persistence.repositories.base_repository import BaseRepository
from src.infrastructure.persistence.repositories.mappers.user import from_orm_to_user


class UserRepository(UserRepositoryInterface, BaseRepository):
    async def get(self, email: Email = None, id: EntityId = None) -> User:
        if email is not None:
            result = await self.db.execute(select(UserOrm).where(UserOrm.email == email))
        elif id is not None:
            result = await self.db.execute(select(UserOrm).where(UserOrm.id == id.value))
        else:
            return None

        user = result.scalar()
        return from_orm_to_user(user) if user else None

    async def save(self, user: User) -> None:
        user = UserOrm(
            id=user.id.value,
            first_name=user.first_name,
            second_name=user.second_name,
            email=user.email,
            hash_password=user.hash_password,
            is_superuser=user.is_superuser,
        )
        self.db.add(user)
        await self.db.commit()
