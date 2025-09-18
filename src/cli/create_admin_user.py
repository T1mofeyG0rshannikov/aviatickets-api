import asyncio
from datetime import date, datetime
from getpass import getpass

from src.application.usecases.user.create import CreateUser
from src.entities.user.value_objects.birth_date import BirthDate
from src.entities.user.value_objects.email import Email
from src.entities.user.value_objects.first_name import FirstName
from src.entities.user.value_objects.password import Password
from src.entities.user.value_objects.second_name import SecondName
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


def read_field(field_name: str, valid_func, read_func=input, mapped_func=str, mapped_func_args=[]) -> str:
    is_valid = False
    while not is_valid:
        try:
            field = mapped_func(read_func(f"Enter {field_name}: "), *mapped_func_args)
        except ValueError as e:
            print(e)
            continue

        is_valid = valid_func(field)
        if not is_valid:
            print(f"""Invalid {field_name} - "{field}". Try again""")

    return field


async def main():
    email = read_field(field_name="email", valid_func=Email.is_valid_email)
    first_name = read_field(field_name="first name", valid_func=FirstName.validation)
    second_name = read_field(field_name="second name", valid_func=SecondName.validation)
    password = read_field(field_name="password", valid_func=Password.validate, read_func=getpass)
    birth_date = read_field(
        field_name="birth date",
        valid_func=BirthDate.validate,
        mapped_func=datetime.strptime,
        mapped_func_args=["%d.%m.%Y"],
    )

    create_user = await UsecasesDIContainer.create_user()

    await create_admin_user(
        email=email,
        password=password,
        first_name=first_name,
        second_name=second_name,
        create_user=create_user,
        birth_date=birth_date,
    )


if __name__ == "__main__":
    asyncio.run(main())
