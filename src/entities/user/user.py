from dataclasses import dataclass

from src.entities.user.value_objects.email import Email
from src.entities.value_objects.entity_id import EntityId


@dataclass
class User:
    id: EntityId
    first_name: str
    second_name: str
    email: Email
    hash_password: str
    is_superuser: bool
    is_active: bool = True

    @classmethod
    def create(
        cls,
        first_name: str,
        second_name: str,
        email: Email,
        hash_password: str,
        is_superuser: bool = False,
        is_active: bool = True,
    ):
        if not first_name:
            raise ValueError("first_name is required")

        if not second_name:
            raise ValueError("second_name is required")

        return cls(
            id=EntityId.generate(),
            first_name=first_name,
            second_name=second_name,
            email=email,
            hash_password=hash_password,
            is_superuser=is_superuser,
            is_active=is_active,
        )
