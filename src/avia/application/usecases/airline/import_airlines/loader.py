from abc import ABC, abstractmethod

from avia.application.dto.airline import CreateAirlineDTO


class AirlinesLoader(ABC):
    @abstractmethod
    def load(self) -> list[CreateAirlineDTO]:
        ...
