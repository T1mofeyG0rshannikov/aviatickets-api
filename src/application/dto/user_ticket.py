from dataclasses import dataclass

from src.application.dto.ticket import TicketFullInfoDTO
from src.entities.user.user import User
from src.entities.user_ticket.user_ticket import Passenger


@dataclass
class UserTicketFullInfoDTO:
    id: int
    user: User
    ticket: TicketFullInfoDTO
    passengers: list[Passenger]


@dataclass
class AdapterPdfField:
    name: str
    value: str
