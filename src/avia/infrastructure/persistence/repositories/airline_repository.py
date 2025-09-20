from collections.abc import Iterable

from sqlalchemy import select

from avia.entities.airline.airline import Airline
from avia.entities.airline.airline_repository import AirlineRepositoryInterface
from avia.entities.airline.value_objects.iata_code import IATACode
from avia.infrastructure.persistence.db.models.models import AirlineOrm
from avia.infrastructure.persistence.persist_base import PersistenceBase
from avia.infrastructure.persistence.repositories.mappers.airline import orm_to_airline


class AirlineRepository(AirlineRepositoryInterface, PersistenceBase):
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

    async def all_iata_codes(self) -> list[IATACode]:
        results = await self.db.execute(select(AirlineOrm.iata))
        codes = results.scalars().all()

        return [IATACode(code) for code in codes]
