from dataclasses import dataclass
from typing import List

from src.entities.user.user import User
from src.entities.user_ticket.user_ticket import Passenger
from src.usecases.tickets.filter.dto import TicketFullInfoDTO


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
