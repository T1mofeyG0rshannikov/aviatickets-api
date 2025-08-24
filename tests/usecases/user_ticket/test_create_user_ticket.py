import datetime
from uuid import UUID

import pytest
from isodate import UTC
from pydantic_core import TzInfo

from src.application.dto.user_ticket import CreatePassengerDTO
from src.application.usecases.create_user_ticket import CreateUserTicket
from src.entities.tickets.exceptions import TicketNotFoundError
from src.entities.user.user import User
from src.entities.value_objects.entity_id import EntityId


@pytest.mark.asyncio
async def test_create_user_ticket(create_user_ticket: CreateUserTicket, populate_db):
    user_mock = User(
        id=EntityId(value=UUID("0c95ad77-07b3-4516-accc-c96647dbbbb8")),
        first_name="Тимофей",
        second_name="Марков",
        email="tgorshannikov@mail.ru",
        hash_password="$2b$12$nfKvEXfUHAgKZRVPLwwD9.4edFLxtpyTF6SoEvqh2i0Ad4AeyiDQW",
        is_superuser=True,
        is_active=True,
    )

    result = await create_user_ticket(
        ticket_id=UUID("fce3917b-2afa-4930-9fed-18b5f79a607d"),
        passengers_to_create=[
            CreatePassengerDTO(
                first_name="string",
                second_name="string",
                gender="string",
                birth_date=datetime.datetime(2025, 8, 22, 22, 24, 45, 740000),
                passport="111111111",
                expiration_date=datetime.date(2026, 8, 22),
            )
        ],
        user=user_mock,
    )

    assert result is None


@pytest.fixture
def mock_create_user_ticket(mock_user_ticket_repository, mock_ticket_repository) -> CreateUserTicket:
    return CreateUserTicket(mock_user_ticket_repository, mock_ticket_repository)


@pytest.mark.asyncio
async def test_create_user_ticket_ticket_not_found(mock_create_user_ticket: CreateUserTicket):
    user_mock = User(
        id=EntityId(value=UUID("0c95ad77-07b3-4516-accc-c96647dbbbb8")),
        first_name="Тимофей",
        second_name="Марков",
        email="tgorshannikov@mail.ru",
        hash_password="$2b$12$nfKvEXfUHAgKZRVPLwwD9.4edFLxtpyTF6SoEvqh2i0Ad4AeyiDQW",
        is_superuser=True,
        is_active=True,
    )

    mock_create_user_ticket.ticket_repository.get.return_value = None

    with pytest.raises(TicketNotFoundError) as excinfo:
        await mock_create_user_ticket(
            ticket_id=UUID("fed25097-d773-4297-94f9-e3243029df9f"),
            passengers_to_create=[
                CreatePassengerDTO(
                    first_name="string",
                    second_name="string",
                    gender="string",
                    birth_date=datetime.datetime(2025, 8, 22, 22, 24, 45, 740000),
                    passport="111111111",
                    expiration_date=datetime.date(2026, 8, 22),
                )
            ],
            user=user_mock,
        )

    assert f"Нет билета с id='fed25097-d773-4297-94f9-e3243029df9f'" in str(excinfo.value)
