from dataclasses import dataclass

from src.entities.value_objects.entity_id import EntityId


@dataclass
class City:
    id: EntityId
    name: str
    name_english: str

    @classmethod
    def create(cls, name: str, name_english: str):
        return cls(id=EntityId.generate(), name=name, name_english=name_english)
