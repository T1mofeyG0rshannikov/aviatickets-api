from src.entities.location.region.region import Region
from src.entities.value_objects.entity_id import EntityId
from src.infrastructure.persistence.db.models.models import RegionOrm


def orm_to_region(region: RegionOrm) -> Region:
    return Region(
        id=EntityId(region.id),
        iso=region.iso,
        name=region.name,
        name_english=region.name_english,
        country_id=EntityId(region.country_id),
    )
