from abc import ABC, abstractmethod

from avia.application.dto.location import CreateCityDTO


class CitiesLoader(ABC):
    @abstractmethod
    def load(self) -> list[CreateCityDTO]:
        ...
