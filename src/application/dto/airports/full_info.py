from dataclasses import dataclass

from src.entities.city.city import City
from src.entities.country.country import Country
from src.entities.region.region import Region


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
    name_russian: str | None = None
