import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from avia.application.usecases.create_user_ticket import CreateUserTicket
from avia.infrastructure.persistence.repositories.tickets_repository import (
    TicketRepository,
)
from avia.infrastructure.persistence.repositories.user_ticket_repository import (
    UserTicketRepository,
)


@pytest.fixture
async def create_user_ticket(
    user_ticket_repository: UserTicketRepository, ticket_repository: TicketRepository, transaction: AsyncSession
) -> CreateUserTicket:
    return CreateUserTicket(
        repository=user_ticket_repository, ticket_repository=ticket_repository, transaction=transaction
    )
