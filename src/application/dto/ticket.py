from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from src.application.dto.airline import AirlineDTO
from src.application.dto.airports.full_info import AirportFullInfoDTO


@dataclass
class TicketSegmentFullInfoDTO:
    id: UUID
    flight_number: str
    segment_number: int
    destination_airport: AirportFullInfoDTO
    origin_airport: AirportFullInfoDTO
    airline: AirlineDTO
    departure_at: datetime
    return_at: datetime
    duration: int
    status: str
    seat_class: str


@dataclass
class TicketFullInfoDTO:
    id: UUID
    duration: int
    price: float
    currency: str
    transfers: int
    segments: list[TicketSegmentFullInfoDTO]
