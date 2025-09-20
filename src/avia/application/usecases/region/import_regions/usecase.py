from avia.application.factories.region_factory import RegionFactory
from avia.application.persistence.bulk_savers.region_saver import (
    RegionBulkSaverInterface,
)
from avia.application.persistence.transaction import Transaction
from avia.application.usecases.region.import_regions.loader import RegionsLoader
from avia.entities.exceptions import DomainError
from avia.entities.location.location_repository import LocationRepositoryInterface
from avia.entities.location.region.iso import ISOCode


class ImportRegions:
    def __init__(
        self,
        loader: RegionsLoader,
        repository: LocationRepositoryInterface,
        importer: RegionBulkSaverInterface,
        transaction: Transaction,
    ) -> None:
        self.loader = loader
        self.repository = repository
        self.importer = importer
        self.transaction = transaction

    async def get_exist_codes(self) -> set[ISOCode]:
        regions = await self.repository.all_regions()
        return {region.iso for region in regions}

    async def __call__(self) -> None:
        parsed_data = await self.loader.load()
        exist_codes = await self.get_exist_codes()

        regions = []

        for data in parsed_data:
            if data.iso not in exist_codes:
                try:
                    regions.append(
                        RegionFactory.create(
                            iso=data.iso, country_id=data.country_id, name=data.name, name_english=data.name_english
                        )
                    )
                except DomainError as e:
                    print(f"Error while building Region: {e}")

        await self.importer.add_many(regions)
        await self.transaction.commit()
