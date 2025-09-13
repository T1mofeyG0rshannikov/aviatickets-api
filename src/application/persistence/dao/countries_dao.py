from abc import ABC, abstractmethod

from src.application.dto.location import CountryWithAirportsDTO


class CountriesDAOInterface(ABC):
    @abstractmethod
    async def filter(self, start_with: str) -> list[CountryWithAirportsDTO]:
        ...
