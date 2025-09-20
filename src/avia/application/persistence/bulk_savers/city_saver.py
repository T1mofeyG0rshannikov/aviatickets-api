from abc import ABC, abstractmethod

from avia.entities.location.city.city import City


class CityBulkSaverInterface(ABC):
    @abstractmethod
    async def add_many(self, cities: list[City]) -> int:
        ...
