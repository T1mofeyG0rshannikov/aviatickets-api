from dataclasses import dataclass
from datetime import date, datetime

from src.entities.user_ticket.exceptions import (
    ExpiredInternationalPassportError,
    InvalidInternationalPassportError,
)


@dataclass(frozen=True)
class InternationalPassport:
    """Value Object for passenger international passport"""

    number: str
    expiration_date: date

    def __post_init__(self):
        if not self.is_valid_passport_number(self.number):
            raise InvalidInternationalPassportError(f"'{self.number}' is not a valid international passport number.")

        if not self.is_valid_expiration_date(self.expiration_date):
            raise ExpiredInternationalPassportError(f"{self.number} is expired")

    @staticmethod
    def is_valid_passport_number(value):
        return isinstance(value, str) and len(value) == 9 and all(s.isdigit() for s in value)

    @staticmethod
    def is_valid_expiration_date(expiration_date: date):
        return expiration_date >= datetime.today().date()
