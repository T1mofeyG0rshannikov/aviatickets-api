from src.application.usecases.create_cities.csv_parser import CitiesCsvParser
from src.infrastructure.repositories.location_repository import LocationRepository


class CreateCities:
    def __init__(self, csv_parser: CitiesCsvParser, repository: LocationRepository) -> None:
        self.csv_parser = csv_parser
        self.repository = repository

    async def get_exist_names(self) -> list[str]:
        cities = await self.repository.all_cities()
        return {city.name for city in cities}

    async def __call__(self, cities: list[list[str]]) -> None:
        parsed_data = self.csv_parser.execute(cities)

        exist_names = await self.get_exist_names()

        create_data = [data for data in parsed_data if data.name not in exist_names]

        return await self.repository.create_cities(cities=create_data)
