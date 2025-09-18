import datetime

from src.application.usecases.user.create import CreateUser
from src.cli.create_admin_user import create_admin_user


async def test_create_admin(create_user: CreateUser):
    result = await create_admin_user(  # type: ignore
        email="testadmin@mail.ru",
        password="zaq123!",
        first_name="Иван",
        second_name="Грозный",
        birth_date=datetime.date(2000, 11, 11),
        create_user=create_user,
    )
    assert result is None
