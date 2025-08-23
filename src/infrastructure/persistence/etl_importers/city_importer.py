from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.etl_importers.city_importer import CityImporterInterface
from src.entities.location.city.city import City
from src.infrastructure.persistence.db.models.models import CityOrm


class CityImporter(CityImporterInterface):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def add_many(self, cities: list[City]) -> int:
        try:
            cities_orms = []
            for city in cities:
                cities_orms.append(CityOrm(id=city.id.value, name=city.name, name_english=city.name_english))

            self.db.add_all(cities_orms)

            await self.db.commit()
            return len(cities_orms)
        except SQLAlchemyError as e:
            await self.db.rollback()
            return 0
