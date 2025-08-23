from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class TicketsFilter:
    price_min: int = None
    price_max: int = None
    airline_ids: list[UUID] = None
    origin_airport_ids: list[UUID] = None
    destination_airport_ids: list[UUID] = None
    duration_min: int = None
    duration_max: int = None
    transfers: int = None
    departure_at: datetime = None
    return_at: datetime = None
