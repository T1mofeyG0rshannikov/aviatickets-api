from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.etl_importers.airline_importer import AirlineImporterInterface
from src.entities.airline.airline import Airline
from src.infrastructure.persistence.db.models.models import AirlineOrm


class AirlineImporter(AirlineImporterInterface):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def add_many(self, airlines: list[Airline]) -> int:
        try:
            airlines_orms = []
            for airline in airlines:
                airlines_orms.append(
                    AirlineOrm(
                        id=airline.id.value,
                        icao=airline.icao,
                        iata=airline.iata,
                        name=airline.name.value,
                        name_russian=airline.name_russian.value,
                    )
                )

            self.db.add_all(airlines_orms)

            await self.db.commit()
            return len(airlines_orms)
        except SQLAlchemyError as e:
            await self.db.rollback()
            return 0
