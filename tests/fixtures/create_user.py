import pytest

from src.application.auth.password_hasher import PasswordHasherInterface
from src.application.usecases.user.create import CreateUser
from src.entities.user.user_repository import UserRepositoryInterface


@pytest.fixture
async def create_user(user_repository: UserRepositoryInterface, password_hasher: PasswordHasherInterface) -> CreateUser:
    return CreateUser(user_repository, password_hasher)
