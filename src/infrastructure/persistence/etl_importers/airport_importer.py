from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.etl_importers.airport_importer import AirportImporterInterface
from src.entities.airport.airport import Airport
from src.infrastructure.persistence.db.models.models import AirportOrm


class AirportImporter(AirportImporterInterface):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def add_many(self, airports: list[Airport]) -> int:
        try:
            airport_orms = []
            for airport in airports:
                airport_orms.append(
                    AirportOrm(
                        id=airport.id.value,
                        name=airport.name,
                        continent=airport.continent,
                        country_id=airport.country_id.value if airport.country_id else None,
                        region_id=airport.region_id.value if airport.region_id else None,
                        city_id=airport.city_id.value if airport.city_id else None,
                        scheduled_service=airport.scheduled_service,
                        icao=airport.icao,
                        iata=airport.iata,
                        gps_code=airport.gps_code,
                        local_code=airport.local_code,
                        name_russian=airport.name_russian,
                    )
                )

            self.db.add_all(airport_orms)

            await self.db.commit()
            return len(airport_orms)
        except SQLAlchemyError as e:
            await self.db.rollback()
            return 0
