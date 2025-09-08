from collections.abc import Iterable

from sqlalchemy import select

from src.entities.airport.airport import Airport
from src.entities.airport.airport_repository import AirportRepositoryInterface
from src.entities.airport.value_objects.iata_code import IATACode
from src.entities.value_objects.entity_id import EntityId
from src.infrastructure.persistence.db.models.models import AirportOrm
from src.infrastructure.persistence.persist_base import PersistBase
from src.infrastructure.persistence.repositories.mappers.airport import orm_to_airport


class AirportRepository(AirportRepositoryInterface, PersistBase):
    async def all(self) -> list[Airport]:
        airports = await self.db.execute(select(AirportOrm))
        return [orm_to_airport(airport) for airport in airports.scalars()]

    async def filter(self, iata_codes: Iterable[IATACode]) -> list[Airport]:
        results = await self.db.execute(select(AirportOrm).where(AirportOrm.iata.in_(iata_codes)))
        airports = results.scalars().all()

        return [orm_to_airport(airport) for airport in airports]

    async def get(self, iata: IATACode | None = None, id: EntityId | None = None) -> Airport | None:
        if iata is not None:
            results = await self.db.execute(select(AirportOrm).where(AirportOrm.iata == iata))
        elif id is not None:
            results = await self.db.execute(select(AirportOrm).where(AirportOrm.id == id))

        airport = results.scalar()

        return orm_to_airport(airport) if airport else None
