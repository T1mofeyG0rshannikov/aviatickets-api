from src.entities.airline.airline import Airline
from src.entities.airline.value_objects.iata_code import IATACode
from src.entities.airline.value_objects.icao_code import ICAOCode
from src.entities.airline.value_objects.name import AirlineName
from src.entities.airline.value_objects.name_russian import AirlineNameRussian
from src.entities.value_objects.entity_id import EntityId
from src.infrastructure.persistence.db.models.models import AirlineOrm


def orm_to_airline(airline: AirlineOrm) -> Airline:
    return Airline(
        id=EntityId(airline.id),
        iata=IATACode(airline.iata),
        icao=ICAOCode(airline.icao),
        name=AirlineName(airline.name),
        name_russian=AirlineNameRussian(airline.name_russian),
    )
