from dataclasses import dataclass
from datetime import datetime

from src.application.dto.airports.full_info import AirportFullInfoDTO
from src.entities.airline.airline import Airline


@dataclass
class TicketSegmentFullInfoDTO:
    id: int
    flight_number: int
    destination_airport: AirportFullInfoDTO
    origin_airport: AirportFullInfoDTO
    airline: Airline
    departure_at: datetime
    return_at: datetime
    duration: int
    status: str
    seat_class: str


@dataclass
class TicketFullInfoDTO:
    id: int
    duration: int
    price: int
    currency: str
    transfers: int
    segments: list[TicketSegmentFullInfoDTO]
