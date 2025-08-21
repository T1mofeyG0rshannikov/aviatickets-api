from dataclasses import dataclass
from datetime import datetime

from src.entities.user_ticket.passport import InternationalPassport


@dataclass
class CreatePassengerDTO:
    first_name: str
    second_name: str

    gender: str
    birth_date: datetime
    passport: InternationalPassport
    expiration_date: datetime

    def __post_init__(self):
        if not isinstance(self.passport, InternationalPassport):
            self.passport = InternationalPassport(self.passport)
