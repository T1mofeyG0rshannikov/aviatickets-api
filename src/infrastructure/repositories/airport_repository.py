from sqlalchemy import insert, select

from src.dto.airport import CreateAirportDTO
from src.entities.airport.airport import Airport
from src.infrastructure.db.mappers.airport import orm_to_airport
from src.infrastructure.db.models.models import AirportOrm
from src.infrastructure.repositories.base_reposiotory import BaseRepository


class AirportRepository(BaseRepository):
    async def create_many(self, airports: list[CreateAirportDTO]) -> None:
        BATCH_SIZE = 5000
        values = [airport.__dict__ for airport in airports]

        for i in range(0, len(values), BATCH_SIZE):
            batch = values[i : i + BATCH_SIZE]
            await self.db.execute(insert(AirportOrm), batch)

        await self.db.commit()

    async def all(self) -> list[Airport]:
        airports = await self.db.execute(select(AirportOrm))
        return [orm_to_airport(airport) for airport in airports.scalars()]

    async def get(self, iata: str = None, id: int = None) -> Airport:
        if iata is not None:
            results = await self.db.execute(select(AirportOrm).where(AirportOrm.iata == iata))
        elif id is not None:
            results = await self.db.execute(select(AirportOrm).where(AirportOrm.id == id))
        return results.scalar()
