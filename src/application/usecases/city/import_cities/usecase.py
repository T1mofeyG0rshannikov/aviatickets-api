from src.application.persistence.bulk_savers.city_saver import CityBulkSaverInterface
from src.application.usecases.city.import_cities.loader import CitiesLoader
from src.entities.location.city.city import City
from src.entities.location.location_repository import LocationRepositoryInterface


class CreateCities:
    def __init__(
        self, loader: CitiesLoader, repository: LocationRepositoryInterface, importer: CityBulkSaverInterface
    ) -> None:
        self.loader = loader
        self.repository = repository
        self.importer = importer

    async def get_exist_names(self) -> set[str]:
        cities = await self.repository.all_cities()
        return {city.name for city in cities}

    async def __call__(self) -> None:
        parsed_data = self.loader.load()

        exist_names = await self.get_exist_names()

        create_data = [
            City.create(name=data.name, name_english=data.name_english)
            for data in parsed_data
            if data.name not in exist_names
        ]

        return await self.importer.add_many(cities=create_data)  # type: ignore
