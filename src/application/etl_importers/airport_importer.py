from abc import ABC, abstractmethod

from src.entities.airport.airport import Airport


class AirportImporterInterface(ABC):
    @abstractmethod
    async def add_many(self, airports: list[Airport]) -> int:
        ...
