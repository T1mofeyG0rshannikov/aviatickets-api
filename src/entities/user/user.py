from dataclasses import dataclass

from src.entities.user.value_objects.email import Email
from src.entities.user.value_objects.first_name import FirstName
from src.entities.user.value_objects.second_name import SecondName
from src.entities.user.value_objects.user_id import UserId


@dataclass
class User:
    id: UserId
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
            id=UserId.generate(),
            first_name=first_name,
            second_name=second_name,
            email=email,
            hash_password=hash_password,
            is_superuser=is_superuser,
            is_active=is_active,
        )

    @property
    def full_name(self) -> str:
        return f"""{self.first_name} {self.second_name}"""
