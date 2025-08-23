from unittest.mock import MagicMock

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
async def mock_ticket_dao() -> TicketDAO:
    return MagicMock(spec=TicketDAO)


@pytest.fixture
async def mock_airport_repository():
    return MagicMock(spec=AirportRepository)


@pytest.fixture
async def mock_location_repository():
    return MagicMock(spec=LocationRepository)


@pytest.fixture
async def mock_user_ticket_repository():
    return MagicMock(spec=UserTicketRepository)


@pytest.fixture
async def mock_user_repository():
    return MagicMock(spec=UserRepository)


@pytest.fixture
async def mock_ticket_repository():
    return MagicMock(spec=TicketRepository)
