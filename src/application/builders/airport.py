from src.application.dto.airports.full_info import AirportFullInfoDTO
from src.infrastructure.db.mappers.city import orm_to_city
from src.infrastructure.db.mappers.country import orm_to_country
from src.infrastructure.db.mappers.region import orm_to_region
from src.infrastructure.db.models.models import AirportOrm


class AirportFullInfoDTOBuilder:
    @classmethod
    def from_orm(cls, airport: AirportOrm) -> AirportFullInfoDTO:
        return AirportFullInfoDTO(
            id=airport.id,
            name=airport.name,
            continent=airport.continent,
            country=orm_to_country(airport.country) if airport.country else None,
            region=orm_to_region(airport.region) if airport.region else None,
            city=orm_to_city(airport.city) if airport.city else None,
            scheduled_service=airport.scheduled_service,
            icao=airport.icao,
            iata=airport.iata,
            gps_code=airport.gps_code,
            name_russian=airport.name_russian,
        )
