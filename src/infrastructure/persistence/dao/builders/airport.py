from src.application.dto.airports.full_info import AirportFullInfoDTO
from src.application.dto.location import CityDTO, CountryDTO, RegionDTO
from src.infrastructure.persistence.db.models.models import AirportOrm


class AirportFullInfoDTOBuilder:
    @classmethod
    def from_orm(cls, airport: AirportOrm) -> AirportFullInfoDTO:
        return AirportFullInfoDTO(
            id=airport.id,
            name=airport.name,
            continent=airport.continent,
            country=CountryDTO(
                id=airport.country.id,
                iso=airport.country.iso,
                name=airport.country.name,
                name_english=airport.country.name_english,
            ),
            region=RegionDTO(
                id=airport.region.id,
                iso=airport.region.iso,
                name=airport.region.name,
                name_english=airport.region.name_english,
            )
            if airport.region
            else None,
            city=CityDTO(id=airport.city.id, name=airport.city.name, name_english=airport.city.name_english),
            scheduled_service=airport.scheduled_service,
            icao=airport.icao,
            iata=airport.iata,
            gps_code=airport.gps_code,
            name_russian=airport.name_russian,
        )
