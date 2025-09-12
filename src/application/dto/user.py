from dataclasses import dataclass
from datetime import date
from uuid import UUID

from src.entities.user.user import User


@dataclass
class RegisterUserDTO:
    email: str
    password: str
    first_name: str
    second_name: str
    birth_date: date
    is_superuser: bool = False


@dataclass
class UserDTO:
    id: UUID
    first_name: str
    second_name: str
    email: str
    birth_date: date

    @classmethod
    def from_entity(cls, user: User):
        return cls(
            id=user.id.value,
            first_name=user.first_name.value,
            second_name=user.second_name.value,
            email=user.email,
            birth_date=user.birth_date.value,
        )
