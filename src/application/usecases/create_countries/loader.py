from abc import ABC, abstractmethod

from src.application.dto.location import CreateCountryDTO


class CountriesLoader(ABC):
    @abstractmethod
    def load() -> list[CreateCountryDTO]:
        ...