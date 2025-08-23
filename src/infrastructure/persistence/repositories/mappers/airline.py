from src.entities.airline.airline import Airline
from src.entities.value_objects.entity_id import EntityId
from src.infrastructure.persistence.db.models.models import AirlineOrm


def orm_to_airline(airline: AirlineOrm) -> Airline:
    return Airline(
        id=EntityId(airline.id),
        iata=airline.iata,
        icao=airline.icao,
        name=airline.name,
        name_russian=airline.name_russian,
    )
