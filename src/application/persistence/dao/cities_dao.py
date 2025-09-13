from abc import ABC, abstractmethod

from src.application.dto.location import CityWithAirportsDTO


class CitiesDAOInterface(ABC):
    @abstractmethod
    async def filter(self, start_with: str) -> list[CityWithAirportsDTO]:
        ...
