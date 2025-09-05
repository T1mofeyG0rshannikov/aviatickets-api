from dataclasses import dataclass

from src.entities.airport.value_objects.iata_code import IATACode
from src.entities.airport.value_objects.icao_code import ICAOCode
from src.entities.airport.value_objects.name import AirportName
from src.entities.airport.value_objects.name_russian import AirportNameRussian
from src.entities.value_objects.entity_id import EntityId


@dataclass
class Airport:
    id: EntityId
    name: AirportName
    continent: str
    scheduled_service: str
    icao: ICAOCode
    iata: IATACode
    gps_code: str
    country_id: EntityId
    city_id: EntityId
    region_id: EntityId
    local_code: str | None = None
    name_russian: AirportNameRussian | None = None

    @classmethod
    def create(
        cls,
        name: AirportName,
        continent: str,
        country_id: EntityId,
        region_id: EntityId,
        city_id: EntityId,
        scheduled_service: str,
        icao: ICAOCode,
        iata: IATACode,
        gps_code: str,
        name_russian: AirportNameRussian | None = None,
    ):
        return cls(
            id=EntityId.generate(),
            name=name,
            continent=continent,
            country_id=country_id,
            region_id=region_id,
            city_id=city_id,
            scheduled_service=scheduled_service,
            icao=icao,
            iata=iata,
            gps_code=gps_code,
            name_russian=name_russian,
        )
