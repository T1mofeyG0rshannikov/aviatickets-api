from collections.abc import Iterable
from typing import Protocol

from avia.entities.airport.airport import Airport
from avia.entities.airport.value_objects.iata_code import IATACode
from avia.entities.value_objects.entity_id import EntityId


class AirportRepositoryInterface(Protocol):
    async def all(self) -> list[Airport]:
        raise NotImplementedError

    async def filter(self, iata_codes: Iterable[IATACode]) -> list[Airport]:
        raise NotImplementedError

    async def get(self, iata: IATACode | None = None, id: EntityId | None = None) -> Airport | None:
        raise NotImplementedError
