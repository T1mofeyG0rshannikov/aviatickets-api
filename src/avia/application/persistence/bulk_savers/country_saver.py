from abc import ABC, abstractmethod

from avia.entities.location.country.country import Country


class CountryBulkSaverInterface(ABC):
    @abstractmethod
    async def add_many(self, countries: list[Country]) -> int:
        ...
