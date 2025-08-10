import asyncio
from getpass import getpass
from typing import Annotated

from src.depends.decorator import inject_dependencies
from src.depends.depends import get_password_hasher
from src.depends.repos_container import ReposContainer
from src.repositories.user_repository import UserRepository
from src.user.password_hasher import PasswordHasher


@inject_dependencies
async def create_admin_user(
    username: str,
    email: str,
    password: str,
    user_repository: Annotated[UserRepository, ReposContainer.user_repository],
    password_hasher: Annotated[PasswordHasher, get_password_hasher],
) -> None:
    hashed_password = password_hasher.hash_password(password)
    await user_repository.create(username=username, email=email, hashed_password=hashed_password, is_superuser=True)
    print(f"User '{username}' successfully created!")


if __name__ == "__main__":
    username = input("Enter username: ")
    email = input("Enter email: ")
    password = getpass("Enter password: ")

    asyncio.run(create_admin_user(username, email, password))
