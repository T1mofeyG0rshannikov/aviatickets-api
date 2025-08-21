from unittest.mock import MagicMock

from src.cmd.create_admin_user import create_admin_user
from src.infrastructure.repositories.user_repository import UserRepository


async def test_create_admin():
    mock_user_repository = MagicMock(spec=UserRepository)
    mock_user_repository.create.return_value = None

    result = await create_admin_user(
        email="testadmin@mail.ru",
        password="zaq123!",
        first_name="Иван",
        second_name="Грозный",
        user_repository=mock_user_repository,
    )
    assert result is None
