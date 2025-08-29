from dataclasses import dataclass
from uuid import UUID

from pydantic import BaseModel


@dataclass
class AirlineDTO:
    id: UUID
    iata: str
    icao: str
    name: str
    name_russian: str


class CreateAirlineDTO(BaseModel):
    iata: str
    icao: str
    name: str
    name_russian: str