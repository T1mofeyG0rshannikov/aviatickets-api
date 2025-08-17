import pytest

from src.infrastructure.repositories.airport_repository import AirportRepository
from src.infrastructure.repositories.location_repository import LocationRepository
from src.infrastructure.repositories.tickets_repository import TicketRepository
from src.infrastructure.repositories.user_repository import UserRepository
from src.infrastructure.repositories.user_ticket_repository import UserTicketRepository
from src.usecases.tickets.filter.repository.tickets_repository import (
    TicketReadRepository,
)


@pytest.fixture
async def ticket_read_repository(db):
    return TicketReadRepository(db)


@pytest.fixture
async def airport_repository(db):
    return AirportRepository(db)


@pytest.fixture
async def location_repository(db):
    return LocationRepository(db)


@pytest.fixture
async def user_ticket_repository(db):
    return UserTicketRepository(db)


@pytest.fixture
async def user_repository(db):
    return UserRepository(db)


@pytest.fixture
async def ticket_repository(db):
    return TicketRepository(db)
