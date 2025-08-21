from dataclasses import dataclass

from src.entities.airport.iata_code import IATACode
from src.entities.airport.icao_code import ICAOCode


@dataclass
class CreateAirportDTO:
    name: str
    continent: str
    country_id: int
    region_id: int
    city_id: int
    scheduled_service: str
    icao: ICAOCode
    iata: IATACode
    gps_code: str
    name_russian: str = None

    def get_unique_code(self) -> tuple[IATACode, ICAOCode]:
        return (self.iata, self.icao)

    def __post__init__(self) -> None:
        if self.icao is not None and not isinstance(self.icao, ICAOCode):
            self.icao = ICAOCode(self.icao)

        if self.iata is not None and not isinstance(self.iata, IATACode):
            self.iata = IATACode(self.iata)
