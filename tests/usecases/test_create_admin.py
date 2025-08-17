from src.cmd.create_admin_user import create_admin_user


async def test_create_admin():
    result = await create_admin_user(
        email="testadmin@mail.ru", password="zaq123!", first_name="Иван", second_name="Грозный"
    )
    assert result is None
