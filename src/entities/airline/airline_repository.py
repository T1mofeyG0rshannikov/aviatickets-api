from collections.abc import Iterable
from typing import Protocol

from src.entities.airline.airline import Airline
from src.entities.airline.iata_code import IATACode


class AirlineRepositoryInterface(Protocol):
    async def get(self, iata: str) -> Airline:
        raise NotImplementedError

    async def all(self) -> list[Airline]:
        raise NotImplementedError

    async def filter(self, iata_codes: Iterable[IATACode]) -> list[Airline]:
        raise NotImplementedError
