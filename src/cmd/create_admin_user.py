import asyncio
from getpass import getpass
from typing import Annotated

from src.application.usecases.user.create import CreateUser
from src.infrastructure.depends.base import get_create_user
from src.infrastructure.depends.decorator import inject_dependencies


@inject_dependencies
async def create_admin_user(
    email: str,
    password: str,
    first_name: str,
    second_name: str,
    create_user: Annotated[CreateUser, get_create_user],
) -> None:
    await create_user(
        email=email,
        password=password,
        first_name=first_name,
        second_name=second_name,
        is_superuser=True,
    )

    print(f"User '{email}' successfully created!")


if __name__ == "__main__":
    email = input("Enter email: ")
    first_name = input("Enter first_name: ")
    second_name = input("Enter second_name: ")

    password = getpass("Enter password: ")

    asyncio.run(create_admin_user(email=email, password=password, first_name=first_name, second_name=second_name))
