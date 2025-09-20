import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from avia.application.auth.password_hasher import PasswordHasherInterface
from avia.application.usecases.user.create import CreateUser
from avia.entities.user.user_repository import UserRepositoryInterface


@pytest.fixture
async def create_user(
    user_repository: UserRepositoryInterface, password_hasher: PasswordHasherInterface, transaction: AsyncSession
) -> CreateUser:
    return CreateUser(user_repository, password_hasher, transaction=transaction)
