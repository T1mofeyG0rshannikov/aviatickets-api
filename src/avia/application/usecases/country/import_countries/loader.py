from abc import ABC, abstractmethod

from avia.application.dto.location import CreateCountryDTO


class CountriesLoader(ABC):
    @abstractmethod
    def load(self) -> list[CreateCountryDTO]:
        ...
