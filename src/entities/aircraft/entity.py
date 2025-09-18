from dataclasses import dataclass

from src.entities.aircraft.value_objects.iata import IATACode
from src.entities.aircraft.value_objects.wtc import AircraftWTC
from src.entities.value_objects.entity_id import EntityId


@dataclass
class Aircraft:
    id: EntityId
    iata: IATACode
    name: str
    wtc: AircraftWTC

    @classmethod
    def create(cls, iata: IATACode, name: str, wtc: AircraftWTC):
        return cls(id=EntityId.generate(), iata=iata, name=name, wtc=wtc)
