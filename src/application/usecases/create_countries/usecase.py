from src.application.usecases.create_countries.csv_parser import CountriesCsvParser
from src.entities.location.country.iso import ISOCode
from src.entities.location.location_repository import LocationRepositoryInterface


class CreateCountries:
    def __init__(self, csv_parser: CountriesCsvParser, repository: LocationRepositoryInterface) -> None:
        self.csv_parser = csv_parser
        self.repository = repository

    async def get_exist_codes(self) -> list[ISOCode]:
        countries = await self.repository.all_countries()
        return {country.iso for country in countries}

    async def __call__(self, countries: list[list[str]]) -> None:
        parsed_data = self.csv_parser.execute(countries)

        exist_codes = await self.get_exist_codes()

        create_data = [data for data in parsed_data if data.iso not in exist_codes]

        return await self.repository.save_countries(countries=create_data)
