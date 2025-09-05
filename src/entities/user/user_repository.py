from typing import Protocol

from src.entities.user.user import User
from src.entities.user.value_objects.email import Email
from src.entities.value_objects.entity_id import EntityId


class UserRepositoryInterface(Protocol):
    async def get(self, email: Email | str | None = None, id: EntityId | None = None) -> User | None:
        raise NotImplementedError

    async def save(self, data: User) -> None:
        raise NotImplementedError
