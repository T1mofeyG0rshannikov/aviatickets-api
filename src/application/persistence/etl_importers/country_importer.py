from abc import ABC, abstractmethod

from src.entities.location.country.country import Country


class CountryImporterInterface(ABC):
    @abstractmethod
    async def add_many(self, countries: list[Country]) -> int:
        ...
