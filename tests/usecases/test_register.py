from datetime import date

import pytest

from avia.application.auth.access_token import AccessToken
from avia.application.dto.user import RegisterUserDTO
from avia.application.usecases.user.auth.register import Register
from avia.application.usecases.user.create import CreateUser
from avia.entities.user.exceptions import UserWithEmailAlreadyExistError
from avia.infrastructure.jwt.jwt_processor import JwtProcessor


@pytest.fixture
async def register(create_user: CreateUser, jwt_processor: JwtProcessor) -> Register:
    return Register(create_user, jwt_processor)


@pytest.mark.asyncio
async def test_register(register: Register):
    result = await register(
        RegisterUserDTO(
            email="newuseremail@mail.ru",
            password="zaq123!",
            first_name="Вася",
            second_name="Смирнов",
            birth_date=date(2000, 1, 1),
        )
    )

    assert isinstance(result, AccessToken)


@pytest.mark.asyncio
async def test_register_not_unique_email(register: Register, populate_db):
    email = "tgorshannikov@mail.ru"
    with pytest.raises(UserWithEmailAlreadyExistError) as excinfo:
        await register(
            RegisterUserDTO(
                email=email, password="zaq123!", first_name="Вася", second_name="Смирнов", birth_date=date(2000, 1, 1)
            )
        )

    assert f"User with email '{email}' already exist" in str(excinfo.value)
