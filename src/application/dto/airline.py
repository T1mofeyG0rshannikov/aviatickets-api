from dataclasses import dataclass
from uuid import UUID


@dataclass
class AirlineDTO:
    id: UUID
    iata: str
    icao: str
    name: str
    name_russian: str
