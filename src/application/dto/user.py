from dataclasses import dataclass
from uuid import UUID


@dataclass
class RegisterUserDTO:
    email: str
    password: str
    first_name: str
    second_name: str
    is_superuser: bool = False


@dataclass
class UserDTO:
    id: UUID
    first_name: str
    second_name: str
    email: str
