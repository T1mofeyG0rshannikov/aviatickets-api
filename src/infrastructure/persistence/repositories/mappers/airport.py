from src.entities.airport.airport import Airport
from src.entities.value_objects.entity_id import EntityId
from src.infrastructure.persistence.db.models.models import AirportOrm


def orm_to_airport(airport: AirportOrm) -> Airport:
    return Airport(
        id=EntityId(airport.id),
        name=airport.name,
        continent=airport.continent,
        country_id=EntityId(airport.country_id),
        region_id=EntityId(airport.region_id),
        city_id=EntityId(airport.city_id),
        scheduled_service=airport.scheduled_service,
        icao=airport.icao,
        iata=airport.iata,
        gps_code=airport.gps_code,
        name_russian=airport.name_russian,
    )
