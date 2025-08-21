from dataclasses import dataclass

from src.entities.user.email import Email


@dataclass
class RegisterUserDTO:
    email: str
    password: str
    first_name: str
    second_name: str


@dataclass
class CreateUserDTO:
    email: Email
    hashed_password: str
    first_name: str
    second_name: str
    is_superuser: bool

    def __post__init__(self) -> None:
        if not isinstance(self.email, Email):
            self.email = Email(self.email)
