from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserTicket:
    id: int
    user_id: int
    ticket_id: int


@dataclass
class Passenger:
    id: int
    gender: str
    first_name: str
    second_name: str
    birth_date: datetime
