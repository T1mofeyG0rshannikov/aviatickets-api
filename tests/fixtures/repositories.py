import pytest

from avia.infrastructure.persistence.dao.filters.filters import SqlalchemyTicketsFilter
from avia.infrastructure.persistence.dao.tickets_dao import TicketDAO
from avia.infrastructure.persistence.repositories.airport_repository import (
    AirportRepository,
)
from avia.infrastructure.persistence.repositories.location_repository import (
    LocationRepository,
)
from avia.infrastructure.persistence.repositories.tickets_repository import (
    TicketRepository,
)
from avia.infrastructure.persistence.repositories.user_repository import UserRepository
from avia.infrastructure.persistence.repositories.user_ticket_repository import (
    UserTicketRepository,
)


@pytest.fixture
def filter_builder() -> SqlalchemyTicketsFilter:
    return SqlalchemyTicketsFilter()


@pytest.fixture
async def ticket_dao(db, filter_builder: SqlalchemyTicketsFilter):
    return TicketDAO(db, filter_builder=filter_builder)


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
