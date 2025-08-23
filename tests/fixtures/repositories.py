import pytest

from src.infrastructure.persistence.dao.tickets_dao import TicketDAO
from src.infrastructure.persistence.repositories.airport_repository import (
    AirportRepository,
)
from src.infrastructure.persistence.repositories.location_repository import (
    LocationRepository,
)
from src.infrastructure.persistence.repositories.tickets_repository import (
    TicketRepository,
)
from src.infrastructure.persistence.repositories.user_repository import UserRepository
from src.infrastructure.persistence.repositories.user_ticket_repository import (
    UserTicketRepository,
)


@pytest.fixture
async def ticket_dao(db):
    return TicketDAO(db)


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
