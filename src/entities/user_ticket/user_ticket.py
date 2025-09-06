from dataclasses import dataclass
from datetime import datetime

from src.entities.user.value_objects.user_id import UserId
from src.entities.user_ticket.value_objects.passport import InternationalPassport
from src.entities.value_objects.entity_id import EntityId


@dataclass
class Passenger:
    id: EntityId
    gender: str
    first_name: str
    second_name: str
    birth_date: datetime
    passport: InternationalPassport

    @classmethod
    def create(
        cls,
        gender: str,
        first_name: str,
        second_name: str,
        birth_date: datetime,
        passport: InternationalPassport,
    ):
        return cls(
            id=EntityId.generate(),
            gender=gender,
            first_name=first_name,
            second_name=second_name,
            birth_date=birth_date,
            passport=passport,
        )


@dataclass
class UserTicket:
    id: EntityId
    user_id: UserId
    ticket_id: EntityId
    passengers: list[Passenger]

    @classmethod
    def create(cls, user_id: UserId, ticket_id: EntityId, passengers: list[Passenger]):
        return cls(id=EntityId.generate(), user_id=user_id, ticket_id=ticket_id, passengers=passengers)
