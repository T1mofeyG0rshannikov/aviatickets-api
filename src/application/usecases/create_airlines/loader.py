from abc import ABC, abstractmethod

from src.application.dto.airline import CreateAirlineDTO


class AirlinesLoader(ABC):
    @abstractmethod
    def load(self) -> list[CreateAirlineDTO]:
        ...