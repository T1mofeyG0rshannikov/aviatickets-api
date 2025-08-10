from dataclasses import dataclass

from src.entities.airline.iata_code import IATACode
from src.entities.airline.icao_code import ICAOCode


@dataclass
class CreateAirlineDTO:
    iata: IATACode
    icao: ICAOCode
    name: str
    name_russian: str

    def __hash__(self):
        return hash((self.iata, self.icao))
