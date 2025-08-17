from dataclasses import dataclass
from datetime import datetime

from src.dto.airport import AirportFullInfoDTO
from src.entities.airline.airline import Airline


@dataclass
class TicketFullInfoDTO:
    id: int
    origin_airport: AirportFullInfoDTO
    destination_airport: AirportFullInfoDTO
    airline: Airline
    departure_at: datetime
    return_at: datetime
    duration: int
    price: int
    transfers: int
