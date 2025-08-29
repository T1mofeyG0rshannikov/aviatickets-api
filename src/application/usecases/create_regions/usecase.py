from src.application.factories.region_factory import RegionFactory
from src.entities.exceptions import DomainError
from src.application.usecases.create_regions.loader import RegionsLoader
from src.application.etl_importers.region_importer import RegionImporterInterface
from src.entities.location.country.iso import ISOCode
from src.entities.location.location_repository import LocationRepositoryInterface


class CreateRegions:
    def __init__(
        self,
        loader: RegionsLoader,
        repository: LocationRepositoryInterface,
        importer: RegionImporterInterface,
    ) -> None:
        self.loader = loader
        self.repository = repository
        self.importer = importer

    async def get_exist_codes(self) -> set[ISOCode]:
        regions = await self.repository.all_regions()
        return {region.iso for region in regions}

    async def __call__(self) -> None:
        parsed_data = await self.loader.load()
        exist_codes = await self.get_exist_codes()

        create_data = []

        for data in parsed_data:
            if data.iso not in exist_codes:
                try:
                    create_data.append(RegionFactory.create(
                        iso=data.iso,
                        country_id=data.country_id,
                        name=data.name,
                        name_english=data.name_english
                    ))
                except DomainError as e:
                    print(F"Error while building Region: {e}")

        return await self.importer.add_many(create_data)
