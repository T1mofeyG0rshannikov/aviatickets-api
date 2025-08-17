import datetime

import pytest

from src.entities.user_ticket.dto import CreatePassengerDTO
from src.infrastructure.repositories.user_repository import UserRepository
from src.usecases.create_user_ticket.usecase import CreateUserTicket


@pytest.mark.asyncio
async def test_create_user_ticket(create_user_ticket: CreateUserTicket, user_repository: UserRepository):
    user = await user_repository.get(id=2)

    result = await create_user_ticket(
        ticket_id=1,
        passangers=[
            CreatePassengerDTO(
                first_name="Тимофей",
                second_name="Марков",
                gender="Мужской",
                birth_date=datetime.datetime(year=2025, month=1, day=1),
            )
        ],
        user=user,
    )

    assert result is None
