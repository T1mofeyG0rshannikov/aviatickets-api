import asyncio
from getpass import getpass

from src.application.usecases.user.create import CreateUser
from src.infrastructure.depends.usecases import UsecasesDIContainer


async def create_admin_user(
    email: str,
    password: str,
    first_name: str,
    second_name: str,
    create_user: CreateUser,
) -> None:
    await create_user(
        email=email,
        password=password,
        first_name=first_name,
        second_name=second_name,
        is_superuser=True,
    )

    print(f"User '{email}' successfully created!")


async def main():
    email = input("Enter email: ")
    first_name = input("Enter first_name: ")
    second_name = input("Enter second_name: ")
    password = getpass("Enter password: ")

    create_user = await UsecasesDIContainer.create_user()

    asyncio.run(
        create_admin_user(
            email=email, password=password, first_name=first_name, second_name=second_name, create_user=create_user
        )
    )


if __name__ == "__main__":
    asyncio.run(main())
