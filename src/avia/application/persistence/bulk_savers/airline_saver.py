from abc import ABC, abstractmethod

from avia.entities.airline.airline import Airline


class AirlineBulkSaverInterface(ABC):
    @abstractmethod
    async def add_many(self, airlines: list[Airline]) -> int:
        ...
