from abc import ABC, abstractmethod

from src.entities.location.city.city import City


class CityImporterInterface(ABC):
    @abstractmethod
    async def add_many(self, cities: list[City]) -> int:
        ...
