from src.application.etl_importers.city_importer import CityImporterInterface
from src.application.usecases.create_cities.csv_parser import CitiesCsvParser
from src.entities.location.location_repository import LocationRepositoryInterface


class CreateCities:
    def __init__(
        self, csv_parser: CitiesCsvParser, repository: LocationRepositoryInterface, importer: CityImporterInterface
    ) -> None:
        self.csv_parser = csv_parser
        self.repository = repository
        self.importer = importer

    async def get_exist_names(self) -> list[str]:
        cities = await self.repository.all_cities()
        return {city.name for city in cities}

    async def __call__(self, cities: list[list[str]]) -> None:
        parsed_data = self.csv_parser.execute(cities)

        exist_names = await self.get_exist_names()

        create_data = [data for data in parsed_data if data.name not in exist_names]

        return await self.importer.add_many(cities=create_data)
