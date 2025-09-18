from typing import Protocol

from src.entities.airline.airline import Airline
from src.entities.airline.value_objects.iata_code import IATACode


class AirlineRepositoryInterface(Protocol):
    async def get(self, iata: IATACode) -> Airline:
        raise NotImplementedError

    async def all(self) -> list[Airline]:
        raise NotImplementedError

    async def all_iata_codes(self) -> list[IATACode]:
        raise NotImplementedError

    async def filter(self, iata_codes: set[IATACode]) -> list[Airline]:
        raise NotImplementedError
