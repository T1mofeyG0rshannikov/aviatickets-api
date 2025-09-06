from src.application.persistence.etl_importers.country_importer import (
    CountryImporterInterface,
)
from src.application.usecases.create_countries.loader import CountriesLoader
from src.entities.location.country.country import Country
from src.entities.location.country.iso import ISOCode
from src.entities.location.location_repository import LocationRepositoryInterface


class CreateCountries:
    def __init__(
        self,
        loader: CountriesLoader,
        repository: LocationRepositoryInterface,
        importer: CountryImporterInterface,
    ) -> None:
        self.loader = loader
        self.repository = repository
        self.importer = importer

    async def get_exist_codes(self) -> set[ISOCode]:
        countries = await self.repository.all_countries()
        return {country.iso for country in countries}

    async def __call__(self) -> None:
        parsed_data = self.loader.load()

        exist_codes = await self.get_exist_codes()

        create_data = [
            Country.create(iso=data.iso, name=data.name, name_english=data.name_english)
            for data in parsed_data
            if data.iso not in exist_codes
        ]

        return await self.importer.add_many(countries=create_data)  # type: ignore
