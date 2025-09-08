from dataclasses import dataclass

from src.entities.location.region.iso import ISOCode
from src.entities.value_objects.entity_id import EntityId


@dataclass
class Region:
    id: EntityId
    iso: ISOCode
    country_id: EntityId
    name: str
    name_english: str

    @classmethod
    def create(cls, iso: ISOCode, name: str, name_english: str, country_id: EntityId):
        return cls(id=EntityId.generate(), iso=iso, name=name, name_english=name_english, country_id=country_id)

    def __hash__(self):
        return hash(self.iso)
