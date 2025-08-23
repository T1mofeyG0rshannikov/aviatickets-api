from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.etl_importers.country_importer import CountryImporterInterface
from src.entities.location.country.country import Country
from src.infrastructure.persistence.db.models.models import CountryOrm


class CountryImporter(CountryImporterInterface):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def add_many(self, countries: list[Country]) -> int:
        try:
            countries_orms = []
            for country in countries:
                countries_orms.append(
                    CountryOrm(
                        id=country.id.value, iso=country.iso, name=country.name, name_english=country.name_english
                    )
                )

            self.db.add_all(countries_orms)

            await self.db.commit()
            return len(countries_orms)
        except SQLAlchemyError as e:
            await self.db.rollback()
            return 0
