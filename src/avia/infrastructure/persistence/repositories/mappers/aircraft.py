from avia.entities.aircraft.entity import Aircraft
from avia.entities.aircraft.value_objects.iata import IATACode
from avia.entities.value_objects.entity_id import EntityId
from avia.infrastructure.persistence.db.models.models import AircraftOrm


def orm_to_aircraft(aircraft: AircraftOrm) -> Aircraft:
    return Aircraft(id=EntityId(value=aircraft.id), name=aircraft.name, iata=IATACode(aircraft.iata), wtc=aircraft.wtc)
