from sqlalchemy import select

from src.entities.aircraft.entity import Aircraft
from src.entities.aircraft.repository import AircraftRepositoryInterface
from src.entities.aircraft.value_objects.iata import IATACode
from src.infrastructure.persistence.db.models.models import AircraftOrm
from src.infrastructure.persistence.persist_base import PersistenceBase
from src.infrastructure.persistence.repositories.mappers.aircraft import orm_to_aircraft


class AircraftRepository(AircraftRepositoryInterface, PersistenceBase):
    async def all_iata_codes(self) -> list[IATACode]:
        codes = await self.db.execute(select(AircraftOrm.iata))
        codes = codes.scalars().all()

        return [IATACode(value=code) for code in codes]

    async def filter(self, iata_codes: set[IATACode]) -> list[Aircraft]:
        aircrafts = await self.db.execute(select(AircraftOrm).where(AircraftOrm.iata.in_(iata_codes)))
        aircrafts = aircrafts.scalars().all()

        return [orm_to_aircraft(aircraft) for aircraft in aircrafts]
