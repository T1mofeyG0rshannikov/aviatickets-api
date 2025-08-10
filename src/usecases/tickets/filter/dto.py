from dataclasses import dataclass
from datetime import datetime

from src.entities.airline.airline import Airline
from src.entities.airport.airport import Airport


@dataclass
class TicketFullInfoDTO:
    id: int
    origin_airport: Airport
    destination_airport: Airport
    airline: Airline
    departure_at: datetime
    return_at: datetime
    duration: int
    price: int
    transfers: int
