from src.entities.region.iso import ISOCode
from src.infrastructure.repositories.location_repository import LocationRepository
from src.usecases.create_regions.adapter import RegionCsvToCreateDTOAdapter
from src.usecases.create_regions.csv_parser import RegionsCsvParser


class CreateRegions:
    def __init__(
        self, csv_parser: RegionsCsvParser, adapter: RegionCsvToCreateDTOAdapter, repository: LocationRepository
    ) -> None:
        self.csv_parser = csv_parser
        self.adapter = adapter
        self.repository = repository

    async def get_exist_codes(self) -> set[ISOCode]:
        regions = await self.repository.all_regions()
        return {region.iso for region in regions}

    async def __call__(self, regions: list[list[str]]) -> None:
        csv_data = self.csv_parser.execute(regions)

        parsed_data = await self.adapter.execute(csv_data)

        exist_codes = await self.get_exist_codes()

        create_data = [data for data in parsed_data if data.iso not in exist_codes]

        return await self.repository.create_regions(create_data)
