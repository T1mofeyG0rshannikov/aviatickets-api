from uuid import UUID

from src.entities.airport.airport import Airport
from src.entities.airport.value_objects.iata_code import IATACode
from src.entities.airport.value_objects.icao_code import ICAOCode
from src.entities.airport.value_objects.name import AirportName
from src.entities.airport.value_objects.name_russian import AirportNameRussian
from src.entities.value_objects.entity_id import EntityId


class AirportFactory:
    @classmethod
    def create(
        cls,
        name: str,
        continent: str,
        country_id: UUID,
        region_id: UUID,
        city_id: UUID,
        scheduled_service: str,
        icao: str,
        iata: str,
        gps_code: str,
        name_russian: str,
    ) -> Airport:
        return Airport.create(
            name=AirportName(name),
            continent=continent,
            country_id=EntityId(country_id) if country_id else None,
            region_id=EntityId(region_id) if region_id else None,
            city_id=EntityId(city_id) if city_id else None,
            scheduled_service=scheduled_service,
            icao=ICAOCode(icao),
            iata=IATACode(iata),
            gps_code=gps_code,
            name_russian=AirportNameRussian(name_russian) if name_russian else None,
        )
