from src.application.persistence.etl_importers.region_importer import (
    RegionImporterInterface,
)
from src.entities.location.region.region import Region


class PersistRegions:
    def __init__(
        self,
        importer: RegionImporterInterface,
    ) -> None:
        self.importer = importer

    async def __call__(self, regions: list[Region]) -> None:
        await self.importer.add_many(regions)
