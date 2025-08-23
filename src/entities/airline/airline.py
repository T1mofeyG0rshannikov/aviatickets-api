from dataclasses import dataclass

from src.entities.airline.iata_code import IATACode
from src.entities.airline.icao_code import ICAOCode
from src.entities.value_objects.entity_id import EntityId


@dataclass
class Airline:
    id: EntityId
    iata: IATACode
    icao: ICAOCode
    name: str
    name_russian: str

    @classmethod
    def create(cls, iata: str, icao: str, name: str, name_russian: str):
        return cls(
            id=EntityId.generate(), iata=IATACode(iata), icao=ICAOCode(icao), name=name, name_russian=name_russian
        )
