import pytest

from src.application.usecases.create_user_ticket import CreateUserTicket
from src.infrastructure.repositories.tickets_repository import TicketRepository
from src.infrastructure.repositories.user_ticket_repository import UserTicketRepository


@pytest.fixture
async def create_user_ticket(
    user_ticket_repository: UserTicketRepository, ticket_repository: TicketRepository
) -> CreateUserTicket:
    return CreateUserTicket(user_ticket_repository, ticket_repository)
