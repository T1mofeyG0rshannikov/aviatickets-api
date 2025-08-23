from dataclasses import dataclass
from datetime import datetime

from src.entities.user_ticket.exceptions import ExpiredInternationalPassportError
from src.entities.user_ticket.passport import InternationalPassport
from src.entities.value_objects.entity_id import EntityId


@dataclass
class UserTicket:
    id: EntityId
    user_id: EntityId
    ticket_id: EntityId

    @classmethod
    def create(cls, user_id: EntityId, ticket_id: EntityId):
        return cls(id=EntityId.generate(), user_id=user_id, ticket_id=ticket_id)


@dataclass
class Passenger:
    id: EntityId
    gender: str
    first_name: str
    second_name: str
    birth_date: datetime
    passport: InternationalPassport
    expiration_date: datetime
    user_ticket_id: EntityId

    @classmethod
    def create(
        cls,
        gender: str,
        first_name: str,
        second_name: str,
        birth_date: datetime,
        passport: str,
        expiration_date: datetime,
        user_ticket_id: EntityId,
    ):
        passport_vo = InternationalPassport(passport)

        if expiration_date.date() <= datetime.today().date():
            raise ExpiredInternationalPassportError(f"{passport} is expired")

        return cls(
            id=EntityId.generate(),
            gender=gender,
            first_name=first_name,
            second_name=second_name,
            birth_date=birth_date,
            passport=passport_vo,
            expiration_date=expiration_date,
            user_ticket_id=user_ticket_id,
        )
