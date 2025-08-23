from abc import ABC, abstractmethod

from src.entities.airline.airline import Airline


class AirlineImporterInterface(ABC):
    @abstractmethod
    async def add_many(self, airlines: list[Airline]) -> int:
        ...
