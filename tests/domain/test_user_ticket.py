import datetime

import pytest

from src.entities.user_ticket.exceptions import (
    ExpiredInternationalPassportError,
    InvalidInternationalPassportError,
)
from src.entities.user_ticket.user_ticket import Passenger
from src.entities.user_ticket.value_objects.passport import InternationalPassport


@pytest.mark.asyncio
async def test_create_user_ticket_with_invalid_passport_number():
    with pytest.raises(InvalidInternationalPassportError) as excinfo:
        Passenger.create(
            first_name="Тимофей",
            second_name="Марков",
            gender="Мужской",
            birth_date=datetime.date(year=2025, month=1, day=1),
            passport=InternationalPassport(
                number="invalid_passport", expiration_date=datetime.date(year=2027, month=1, day=1)
            ),
        )

    assert "'invalid_passport' is not a valid international passport number" in str(excinfo.value)


@pytest.mark.asyncio
async def test_create_user_ticket_with_expired_passport():
    passport_number = "123456789"
    with pytest.raises(ExpiredInternationalPassportError) as excinfo:
        Passenger.create(
            first_name="Тимофей",
            second_name="Марков",
            gender="Мужской",
            birth_date=datetime.date(year=2025, month=1, day=1),
            passport=InternationalPassport(
                number=passport_number, expiration_date=datetime.date(year=2025, month=1, day=1)
            ),
        )

    assert f"{passport_number} is expired" in str(excinfo.value)
