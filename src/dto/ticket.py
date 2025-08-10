from dataclasses import dataclass
from datetime import datetime


@dataclass
class CreateAviaTicketDTO:
    origin_airport_id: int
    destination_airport_id: int
    airline_id: int
    departure_at: datetime
    return_at: datetime
    duration: int
    price: int
    transfers: int

    def __hash__(self):
        return hash(
            (
                self.origin_airport_id,
                self.destination_airport_id,
                self.airline_id,
                self.departure_at,
                self.return_at,
                self.duration,
                self.price,
                self.transfers,
            )
        )
