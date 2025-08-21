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

    def __post__init__(self) -> None:
        if self.iata is not None and not isinstance(self.iata, IATACode):
            self.iata = IATACode(self.iata)

        if self.icao is not None and not isinstance(self.icao, ICAOCode):
            self.icao = ICAOCode(self.icao)
