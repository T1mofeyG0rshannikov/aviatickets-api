from dataclasses import dataclass

from src.entities.user.value_objects.email import Email
from src.entities.user.value_objects.first_name import FirstName
from src.entities.user.value_objects.second_name import SecondName
from src.entities.value_objects.entity_id import EntityId


@dataclass
class User:
    id: EntityId
    first_name: FirstName
    second_name: SecondName
    email: Email
    hash_password: str
    is_superuser: bool
    is_active: bool = True

    @classmethod
    def create(
        cls,
        first_name: FirstName,
        second_name: SecondName,
        email: Email,
        hash_password: str,
        is_superuser: bool = False,
        is_active: bool = True,
    ):
        return cls(
            id=EntityId.generate(),
            first_name=first_name,
            second_name=second_name,
            email=email,
            hash_password=hash_password,
            is_superuser=is_superuser,
            is_active=is_active,
        )
