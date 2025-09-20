from typing import Protocol

from avia.entities.aircraft.entity import Aircraft
from avia.entities.aircraft.value_objects.iata import IATACode


class AircraftRepositoryInterface(Protocol):
    async def all_iata_codes(self) -> list[IATACode]:
        raise NotImplementedError

    async def filter(self, iata_codes: set[IATACode]) -> list[Aircraft]:
        raise NotImplementedError
