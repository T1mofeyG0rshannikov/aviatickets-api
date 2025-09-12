import datetime
from uuid import UUID

import pytest
import usecases.user_ticket.mocks as mocks

from src.application.dto.user_ticket import CreatePassengerDTO
from src.application.usecases.create_user_ticket import CreateUserTicket
from src.entities.tickets.exceptions import TicketNotFoundError
from src.entities.value_objects.entity_id import EntityId


@pytest.mark.asyncio
async def test_create_user_ticket(create_user_ticket: CreateUserTicket, populate_db):
    user_mock = mocks.MOCK_USER

    result = await create_user_ticket(  # type: ignore
        ticket_id=EntityId(value=UUID("7d7d949f-f907-4c66-a72e-84f9bb84efba")),
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
    user_mock = mocks.MOCK_USER

    mock_create_user_ticket.ticket_repository.get.return_value = None  # type: ignore

    ticket_id = "fed25097-d773-4297-94f9-e3243029df9f"
    with pytest.raises(TicketNotFoundError) as excinfo:
        await mock_create_user_ticket(
            ticket_id=EntityId(value=UUID(ticket_id)),
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

    assert f"Нет билета с id='{ticket_id}'" in str(excinfo.value)
