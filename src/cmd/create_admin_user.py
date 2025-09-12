import asyncio
from datetime import date, datetime
from getpass import getpass

from src.application.usecases.user.create import CreateUser
from src.infrastructure.depends.usecases import UsecasesDIContainer


async def create_admin_user(
    email: str,
    password: str,
    first_name: str,
    second_name: str,
    birth_date: date,
    create_user: CreateUser,
) -> None:
    await create_user(
        email=email,
        password=password,
        first_name=first_name,
        second_name=second_name,
        birth_date=birth_date,
        is_superuser=True,
    )

    print(f"User '{email}' successfully created!")


async def main():
    email = input("Enter email: ")
    first_name = input("Enter first_name: ")
    second_name = input("Enter second_name: ")
    password = getpass("Enter password: ")
    birth_date = input("Enter your birth date in format dd.mm.yyyy: ")

    create_user = await UsecasesDIContainer.create_user()

    await create_admin_user(
        email=email,
        password=password,
        first_name=first_name,
        second_name=second_name,
        create_user=create_user,
        birth_date=datetime.strptime(birth_date, "%d.%m.%Y"),
    )


if __name__ == "__main__":
    asyncio.run(main())
