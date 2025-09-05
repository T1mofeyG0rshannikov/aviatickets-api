from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID

from src.application.dto.ticket import TicketFullInfoDTO
from src.application.dto.user import UserDTO


@dataclass
class PassengerDTO:
    id: UUID
    gender: str
    first_name: str
    second_name: str


@dataclass
class UserTicketFullInfoDTO:
    id: UUID
    user: UserDTO
    ticket: TicketFullInfoDTO
    passengers: list[PassengerDTO]


@dataclass
class CreatePassengerDTO:
    first_name: str
    second_name: str

    gender: str
    birth_date: datetime
    passport: str
    expiration_date: date
