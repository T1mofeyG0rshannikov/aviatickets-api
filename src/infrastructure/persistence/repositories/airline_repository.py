from collections.abc import Iterable

from sqlalchemy import select

from src.entities.airline.airline import Airline
from src.entities.airline.airline_repository import AirlineRepositoryInterface
from src.entities.airline.value_objects.iata_code import IATACode
from src.infrastructure.persistence.db.models.models import AirlineOrm
from src.infrastructure.persistence.repositories.base_repository import BaseRepository
from src.infrastructure.persistence.repositories.mappers.airline import orm_to_airline


class AirlineRepository(AirlineRepositoryInterface, BaseRepository):
    async def get(self, iata: IATACode) -> Airline:
        results = await self.db.execute(select(AirlineOrm).where(AirlineOrm.iata == iata))
        airline = results.scalar()
        return orm_to_airline(airline)

    async def all(self) -> list[Airline]:
        results = await self.db.execute(select(AirlineOrm))
        airlines = results.scalars().all()
        return [orm_to_airline(airline) for airline in airlines]

    async def filter(self, iata_codes: Iterable[IATACode]) -> list[Airline]:
        results = await self.db.execute(select(AirlineOrm).where(AirlineOrm.iata.in_(iata_codes)))
        airlines = results.scalars().all()

        return [orm_to_airline(airline) for airline in airlines]

    async def create_many(self, airlines: list[Airline]) -> None:
        airlines_orm = [
            AirlineOrm(
                id=airline.id.value,
                icao=airline.icao,
                iata=airline.iata,
                name=airline.name,
                name_russian=airline.name_russian,
            )
            for airline in airlines
        ]

        self.db.add_all(airlines_orm)
        await self.db.commit()
