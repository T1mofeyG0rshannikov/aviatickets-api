from src.application.usecases.country.import_countries.loader import CountriesLoader
from src.application.usecases.country.persist_countries import PersistCountries
from src.entities.location.country.country import Country
from src.entities.location.country.iso import ISOCode
from src.entities.location.location_repository import LocationRepositoryInterface


class ImportCountries:
    def __init__(
        self, loader: CountriesLoader, repository: LocationRepositoryInterface, persist_countries: PersistCountries
    ) -> None:
        self.loader = loader
        self.repository = repository
        self.persist_countries = persist_countries

    async def get_exist_codes(self) -> set[ISOCode]:
        countries = await self.repository.all_countries()
        return {country.iso for country in countries}

    async def __call__(self) -> None:
        parsed_data = self.loader.load()

        exist_codes = await self.get_exist_codes()

        countries = [
            Country.create(iso=data.iso, name=data.name, name_english=data.name_english)
            for data in parsed_data
            if data.iso not in exist_codes
        ]

        return await self.persist_countries(countries)  # type: ignore
