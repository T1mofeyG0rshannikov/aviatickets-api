from collections.abc import Iterable
from typing import Protocol

from src.entities.airport.airport import Airport
from src.entities.airport.iata_code import IATACode


class AirportRepositoryInterface(Protocol):
    async def all(self) -> list[Airport]:
        raise NotImplementedError

    async def filter(self, iata_codes: Iterable[IATACode]) -> list[Airport]:
        raise NotImplementedError

    async def get(self, iata: str = None, id: int = None) -> Airport:
        raise NotImplementedError
