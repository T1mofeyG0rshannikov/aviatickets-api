from src.entities.aircraft.entity import Aircraft
from src.entities.aircraft.value_objects.iata import IATACode
from src.entities.value_objects.entity_id import EntityId
from src.infrastructure.persistence.db.models.models import AircraftOrm


def orm_to_aircraft(aircraft: AircraftOrm) -> Aircraft:
    return Aircraft(id=EntityId(value=aircraft.id), name=aircraft.name, iata=IATACode(aircraft.iata), wtc=aircraft.wtc)
