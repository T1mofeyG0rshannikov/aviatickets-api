from dataclasses import dataclass

from avia.entities.aircraft.value_objects.iata import IATACode
from avia.entities.aircraft.value_objects.wtc import AircraftWTC
from avia.entities.value_objects.entity_id import EntityId


@dataclass
class Aircraft:
    id: EntityId
    iata: IATACode
    name: str
    wtc: AircraftWTC

    @classmethod
    def create(cls, iata: IATACode, name: str, wtc: AircraftWTC):
        return cls(id=EntityId.generate(), iata=iata, name=name, wtc=wtc)
