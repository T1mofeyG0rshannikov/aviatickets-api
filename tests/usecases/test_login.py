import pytest

from src.application.auth.access_token import AccessToken
from src.application.usecases.user.auth.login import Login
from src.entities.exceptions import AccessDeniedError
from src.entities.user.exceptions import InvalidPasswordError, UserNotFoundError
from src.infrastructure.jwt.jwt_processor import JwtProcessor
from src.infrastructure.persistence.repositories.user_repository import UserRepository
from src.infrastructure.security.password_hasher import PasswordHasher


@pytest.fixture
async def login(user_repository: UserRepository, jwt_processor: JwtProcessor, password_hasher: PasswordHasher) -> Login:
    return Login(user_repository, jwt_processor, password_hasher)


@pytest.mark.asyncio
async def test_login(login: Login, populate_db):
    result = await login(email="tgorshannikov@mail.ru", password="zaq123!")
    assert isinstance(result, AccessToken)


@pytest.mark.asyncio
async def test_login_user_not_found(login: Login, populate_db):
    email = "dimapetrov@mail.ru"
    with pytest.raises(UserNotFoundError) as excinfo:
        await login(email=email, password="zaq123!")

    assert f"нет пользователя с email адресом {email}" in str(excinfo.value)


@pytest.mark.asyncio
async def test_login_user_wrong_password(login: Login, populate_db):
    with pytest.raises(InvalidPasswordError) as excinfo:
        await login(email="tgorshannikov@mail.ru", password="ekwngwnpw")

    assert "Неверный пароль" in str(excinfo.value)


@pytest.mark.asyncio
async def test_login_admin_user(login: Login, populate_db):
    result = await login(email="tgorshannikov@mail.ru", password="zaq123!", superuser_required=True)

    assert isinstance(result, AccessToken)


@pytest.mark.asyncio
async def test_login_permission_denied_admin_user(login: Login, populate_db):
    with pytest.raises(AccessDeniedError) as excinfo:
        await login(email="vasyaivanov@mail.ru", password="zaq123!", superuser_required=True)

    assert "Пользователь не является админом" in str(excinfo.value)
