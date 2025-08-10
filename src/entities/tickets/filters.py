from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class TicketsFilter:
    price_min: int = None
    price_max: int = None
    airline_ids: list[int] = None
    origin_airport_ids: list[int] = None
    destination_airport_ids: list[int] = None
    duration_min: int = None
    duration_max: int = None
    transfers: int = None
    departure_at: datetime = None
    return_at: datetime = None
