from avia.application.persistence.bulk_savers.country_saver import (
    CountryBulkSaverInterface,
)
from avia.application.persistence.transaction import Transaction
from avia.application.usecases.country.import_countries.loader import CountriesLoader
from avia.entities.location.country.country import Country
from avia.entities.location.country.iso import ISOCode
from avia.entities.location.location_repository import LocationRepositoryInterface


class ImportCountries:
    def __init__(
        self,
        loader: CountriesLoader,
        repository: LocationRepositoryInterface,
        country_bulk_saver: CountryBulkSaverInterface,
        transaction: Transaction,
    ) -> None:
        self.transaction = transaction
        self.loader = loader
        self.repository = repository
        self.saver = country_bulk_saver

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

        await self.saver.add_many(countries)
        await self.transaction.commit()
