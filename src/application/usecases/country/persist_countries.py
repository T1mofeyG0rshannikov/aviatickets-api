from src.application.persistence.etl_importers.country_importer import (
    CountryImporterInterface,
)
from src.entities.location.country.country import Country


class PersistCountries:
    def __init__(
        self,
        importer: CountryImporterInterface,
    ) -> None:
        self.importer = importer

    async def __call__(self, countries: list[Country]) -> None:
        await self.importer.add_many(countries)
