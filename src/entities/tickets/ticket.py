from dataclasses import dataclass
from datetime import datetime


@dataclass
class Ticket:
    id: int
    origin_airport_id: int
    destination_airport_id: int
    airline_id: int
    departure_at: datetime
    return_at: datetime
    duration: int
    price: int
    transfers: int
