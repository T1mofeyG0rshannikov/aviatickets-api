from dataclasses import dataclass
from datetime import datetime


@dataclass
class CreateTicketSegmentDTO:
    flight_number: str
    origin_airport_id: int
    destination_airport_id: int
    airline_id: int
    departure_at: datetime
    return_at: datetime
    duration: int
    seat_class: str = "economy"
    status: str = "confirmed"


@dataclass
class CreateAviaTicketDTO:
    duration: int
    price: int
    currency: str
    transfers: int
    segments: list[CreateTicketSegmentDTO]

    def __hash__(self):
        return hash(segment.flight_number for segment in self.segments)
