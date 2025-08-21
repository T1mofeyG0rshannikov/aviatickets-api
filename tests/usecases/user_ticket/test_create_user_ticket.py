import datetime

import pytest

from src.application.usecases.create_user_ticket import CreateUserTicket
from src.entities.user_ticket.dto import CreatePassengerDTO
from src.entities.user_ticket.exceptions import ExpiredInternationalPassportError
from src.infrastructure.repositories.user_repository import UserRepository


@pytest.mark.asyncio
async def test_create_user_ticket(create_user_ticket: CreateUserTicket, user_repository: UserRepository):
    user = await user_repository.get(id=2)

    result = await create_user_ticket(
        ticket_id=194,
        passangers=[
            CreatePassengerDTO(
                first_name="Тимофей",
                second_name="Марков",
                gender="Мужской",
                birth_date=datetime.datetime(year=2025, month=1, day=1),
                passport="123456789",
                expiration_date=datetime.datetime(year=3025, month=1, day=1),
            )
        ],
        user=user,
    )

    assert result is None


@pytest.mark.asyncio
async def test_create_user_ticket_with_invalid_passport_number(
    create_user_ticket: CreateUserTicket, user_repository: UserRepository
):
    user = await user_repository.get(id=2)

    with pytest.raises(ValueError) as excinfo:
        await create_user_ticket(
            ticket_id=194,
            passangers=[
                CreatePassengerDTO(
                    first_name="Тимофей",
                    second_name="Марков",
                    gender="Мужской",
                    birth_date=datetime.datetime(year=2025, month=1, day=1),
                    passport="invalid_passport",
                    expiration_date=datetime.datetime(year=2025, month=1, day=1),
                )
            ],
            user=user,
        )

    assert "'invalid_passport' is not a valid international passport number" in str(excinfo.value)


@pytest.mark.asyncio
async def test_create_user_ticket_with_expired_passport(
    create_user_ticket: CreateUserTicket, user_repository: UserRepository
):
    user = await user_repository.get(id=2)

    with pytest.raises(ExpiredInternationalPassportError) as excinfo:
        await create_user_ticket(
            ticket_id=194,
            passangers=[
                CreatePassengerDTO(
                    first_name="Тимофей",
                    second_name="Марков",
                    gender="Мужской",
                    birth_date=datetime.datetime(year=2025, month=1, day=1),
                    passport="123456789",
                    expiration_date=datetime.datetime(year=2025, month=1, day=1),
                )
            ],
            user=user,
        )

    assert f"У пассажира Тимофей Марков истёк срок загран. паспорта" in str(excinfo.value)
