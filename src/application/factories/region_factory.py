from uuid import UUID

from src.entities.location.region.iso import ISOCode
from src.entities.location.region.region import Region
from src.entities.value_objects.entity_id import EntityId


class RegionFactory:
    @classmethod
    def create(cls, iso: str, name: str, name_english: str, country_id: UUID) -> Region:
        return Region.create(
            iso=ISOCode(iso),
            name=name,
            name_english=name_english,
            country_id=EntityId(country_id),
        )
