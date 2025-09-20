from dataclasses import dataclass

from avia.entities.airline.value_objects.iata_code import IATACode
from avia.entities.airline.value_objects.icao_code import ICAOCode
from avia.entities.airline.value_objects.name import AirlineName
from avia.entities.airline.value_objects.name_russian import AirlineNameRussian
from avia.entities.value_objects.entity_id import EntityId


@dataclass
class Airline:
    id: EntityId
    iata: IATACode
    icao: ICAOCode
    name: AirlineName
    name_russian: AirlineNameRussian

    @classmethod
    def create(cls, iata: IATACode, icao: ICAOCode, name: AirlineName, name_russian: AirlineNameRussian):
        return cls(id=EntityId.generate(), iata=iata, icao=icao, name=name, name_russian=name_russian)
