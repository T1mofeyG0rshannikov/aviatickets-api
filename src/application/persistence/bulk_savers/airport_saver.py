from abc import ABC, abstractmethod

from src.entities.airport.airport import Airport


class AirportBulkSaverInterface(ABC):
    @abstractmethod
    async def add_many(self, airports: list[Airport]) -> int:
        ...
