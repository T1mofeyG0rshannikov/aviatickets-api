from dataclasses import dataclass

from src.entities.location.country.iso import ISOCode
from src.entities.value_objects.entity_id import EntityId


@dataclass
class Country:
    id: EntityId
    iso: ISOCode
    name: str
    name_english: str

    @classmethod
    def create(cls, iso: str, name: str, name_english: str):
        return cls(id=EntityId.generate(), iso=ISOCode(iso), name=name, name_english=name_english)
