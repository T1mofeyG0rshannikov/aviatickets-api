import datetime
from uuid import UUID

import pytest

from src.application.dto.user_ticket import CreatePassengerDTO
from src.application.usecases.create_user_ticket import CreateUserTicket
from src.entities.user.user import User
from src.entities.user_ticket.exceptions import (
    ExpiredInternationalPassportError,
    InvalidInternationalPassportError,
)
from src.entities.user_ticket.user_ticket import Passenger
from src.entities.value_objects.entity_id import EntityId
from src.infrastructure.persistence.repositories.user_repository import UserRepository


@pytest.mark.asyncio
async def test_create_user_ticket_with_invalid_passport_number():
    with pytest.raises(InvalidInternationalPassportError) as excinfo:
        Passenger.create(
            first_name="Тимофей",
            second_name="Марков",
            gender="Мужской",
            birth_date=datetime.datetime(year=2025, month=1, day=1),
            passport="invalid_passport",
            expiration_date=datetime.datetime(year=2027, month=1, day=1),
        )

    assert "'invalid_passport' is not a valid international passport number" in str(excinfo.value)


@pytest.mark.asyncio
async def test_create_user_ticket_with_expired_passport():
    with pytest.raises(ExpiredInternationalPassportError) as excinfo:
        Passenger.create(
            first_name="Тимофей",
            second_name="Марков",
            gender="Мужской",
            birth_date=datetime.datetime(year=2025, month=1, day=1),
            passport="123456789",
            expiration_date=datetime.datetime(year=2025, month=1, day=1),
        )

    assert f"У пассажира Тимофей Марков истёк срок загран. паспорта" in str(excinfo.value)
