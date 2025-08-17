from dataclasses import dataclass

from src.entities.airport.iata_code import IATACode
from src.entities.airport.icao_code import ICAOCode
from src.entities.city import City
from src.entities.country.country import Country
from src.entities.region.region import Region


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


@dataclass
class AirportFullInfoDTO:
    id: int
    name: str
    continent: str
    country: Country
    region: Region
    city: City
    scheduled_service: str
    icao: str
    iata: str
    gps_code: str
    name_russian: str = None
