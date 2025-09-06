from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.persistence.etl_importers.region_importer import (
    RegionImporterInterface,
)
from src.entities.location.region.region import Region
from src.infrastructure.persistence.db.models.models import RegionOrm


class RegionImporter(RegionImporterInterface):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def add_many(self, regions: list[Region]) -> int:
        try:
            regions_orms = []
            for region in regions:
                regions_orms.append(
                    RegionOrm(
                        id=region.id.value,
                        iso=region.iso,
                        name=region.name,
                        name_english=region.name_english,
                        country_id=region.country_id.value if region.country_id else None,
                    )
                )

            self.db.add_all(regions_orms)

            await self.db.commit()
            return len(regions_orms)
        except SQLAlchemyError as e:
            await self.db.rollback()
            return 0
