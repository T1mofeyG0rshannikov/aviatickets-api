from typing import Protocol

from src.entities.aircraft.entity import Aircraft
from src.entities.aircraft.value_objects.iata import IATACode


class AircraftRepositoryInterface(Protocol):
    async def all_iata_codes(self) -> list[IATACode]:
        raise NotImplementedError

    async def filter(self, iata_codes: set[IATACode]) -> list[Aircraft]:
        raise NotImplementedError
