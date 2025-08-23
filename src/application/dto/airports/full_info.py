from dataclasses import dataclass
from uuid import UUID

from src.application.dto.location import CityDTO, CountryDTO, RegionDTO


@dataclass
class AirportFullInfoDTO:
    id: UUID
    name: str
    continent: str
    country: CountryDTO
    region: RegionDTO | None = None
    city: CityDTO
    scheduled_service: str
    icao: str
    iata: str
    gps_code: str
    name_russian: str | None = None
