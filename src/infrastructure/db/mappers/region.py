from src.entities.region.region import Region
from src.infrastructure.db.models.models import RegionOrm


def orm_to_region(region: RegionOrm) -> Region:
    return Region(id=region.id, iso=region.iso, name=region.name, name_english=region.name_english)
