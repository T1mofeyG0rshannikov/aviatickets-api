from typing import Protocol

from src.entities.user.user import User
from src.entities.user.value_objects.email import Email
from src.entities.user.value_objects.user_id import UserId
from src.entities.value_objects.entity_id import EntityId


class UserRepositoryInterface(Protocol):
    async def get(self, email: Email | str | None = None, id: UserId | None = None) -> User | None:
        raise NotImplementedError

    async def save(self, data: User) -> None:
        raise NotImplementedError
