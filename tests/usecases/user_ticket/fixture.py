import pytest

from src.infrastructure.repositories.tickets_repository import TicketRepository
from src.infrastructure.repositories.user_ticket_repository import UserTicketRepository
from src.usecases.create_user_ticket.usecase import CreateUserTicket


@pytest.fixture
async def create_user_ticket(
    user_ticket_repository: UserTicketRepository, ticket_repository: TicketRepository
) -> CreateUserTicket:
    return CreateUserTicket(user_ticket_repository, ticket_repository)
