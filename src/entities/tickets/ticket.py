from dataclasses import dataclass
from datetime import datetime


@dataclass
class TicketSegment:
    id: int
    flight_number: int
    origin_airport_id: int
    destination_airport_id: int
    airline_id: int
    departure_at: datetime
    return_at: datetime
    duration: int
    seat_class: str
    status: str


@dataclass
class Ticket:
    id: int
    duration: int
    price: int
    currency: str
    transfers: int
    segments: list[TicketSegment]
