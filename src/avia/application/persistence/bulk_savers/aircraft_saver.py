from abc import ABC, abstractmethod

from avia.entities.aircraft.entity import Aircraft


class AircraftBulkSaverInterface(ABC):
    @abstractmethod
    async def add_many(self, objects: list[Aircraft]) -> int:
        ...
