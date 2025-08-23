from dataclasses import dataclass

from src.entities.airport.iata_code import IATACode
from src.entities.airport.icao_code import ICAOCode
from src.entities.value_objects.entity_id import EntityId


@dataclass
class Airport:
    id: EntityId
    name: str
    continent: str
    scheduled_service: str
    icao: ICAOCode
    iata: IATACode
    gps_code: str
    country_id: EntityId = None
    city_id: EntityId = None
    region_id: EntityId = None
    local_code: str = None
    name_russian: str = None

    @classmethod
    def create(
        cls,
        name: str,
        continent: str,
        country_id: EntityId,
        region_id: EntityId,
        city_id: EntityId,
        scheduled_service: str,
        icao: str,
        iata: str,
        gps_code: str,
        name_russian: str = None,
    ):
        return cls(
            id=EntityId.generate(),
            name=name,
            continent=continent,
            country_id=country_id,
            region_id=region_id,
            city_id=city_id,
            scheduled_service=scheduled_service,
            icao=ICAOCode(icao),
            iata=IATACode(iata),
            gps_code=gps_code,
            name_russian=name_russian,
        )
