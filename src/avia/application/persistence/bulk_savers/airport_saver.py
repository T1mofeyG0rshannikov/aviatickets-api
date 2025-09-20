from abc import ABC, abstractmethod

from avia.entities.airport.airport import Airport


class AirportBulkSaverInterface(ABC):
    @abstractmethod
    async def add_many(self, airports: list[Airport]) -> int:
        ...
