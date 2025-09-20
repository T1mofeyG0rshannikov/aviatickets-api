from abc import ABC, abstractmethod

from avia.application.dto.location import CountryWithAirportsDTO


class CountriesDAOInterface(ABC):
    @abstractmethod
    async def filter(self, start_with: str) -> list[CountryWithAirportsDTO]:
        ...
