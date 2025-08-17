import asyncio
from getpass import getpass
from typing import Annotated

from src.depends.decorator import inject_dependencies
from src.depends.depends import get_password_hasher
from src.depends.repos_container import ReposContainer
from src.entities.user.dto import CreateUserDTO
from src.entities.user.email import Email
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.security.password_hasher import PasswordHasher


@inject_dependencies
async def create_admin_user(
    email: str,
    password: str,
    first_name: str,
    second_name: str,
    user_repository: Annotated[UserRepository, ReposContainer.user_repository],
    password_hasher: Annotated[PasswordHasher, get_password_hasher],
) -> None:
    hashed_password = password_hasher.hash_password(password)
    create_dto = CreateUserDTO(
        email=Email(email),
        hashed_password=hashed_password,
        first_name=first_name,
        second_name=second_name,
        is_superuser=True,
    )

    await user_repository.create(create_dto)
    print(f"User '{email}' successfully created!")


if __name__ == "__main__":
    email = input("Enter email: ")
    first_name = input("Enter first_name: ")
    second_name = input("Enter second_name: ")

    password = getpass("Enter password: ")

    asyncio.run(create_admin_user(email=email, password=password, first_name=first_name, second_name=second_name))
