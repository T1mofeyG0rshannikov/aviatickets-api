from dataclasses import dataclass

from src.entities.airline.iata_code import IATACode
from src.entities.airline.icao_code import ICAOCode


@dataclass
class Airline:
    id: int
    iata: IATACode
    icao: ICAOCode
    name: str
    name_russian: str
