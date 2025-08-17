import pytest

from src.entities.user.access_token import AccessToken
from src.entities.user.dto import RegisterUserDTO
from src.entities.user.exceptions import UserWithEmailAlreadyExistError
from src.infrastructure.jwt.jwt_processor import JwtProcessor
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.security.password_hasher import PasswordHasher
from src.usecases.user.register import Register


@pytest.fixture
async def register(
    user_repository: UserRepository, jwt_processor: JwtProcessor, password_hasher: PasswordHasher
) -> Register:
    return Register(user_repository, jwt_processor, password_hasher)


@pytest.mark.asyncio
async def test_register(register: Register):
    result = await register(
        RegisterUserDTO(email="newuseremail@mail.ru", password="zaq123!", first_name="Вася", second_name="Смирнов")
    )

    assert isinstance(result, AccessToken)


@pytest.mark.asyncio
async def test_register_not_unique_email(register: Register):
    email = "tgorshannikov@mail.ru"
    with pytest.raises(UserWithEmailAlreadyExistError) as excinfo:
        await register(RegisterUserDTO(email=email, password="zaq123!", first_name="Вася", second_name="Смирнов"))

    assert f"Пользователь с почтой '{email}' уже существует" in str(excinfo)
