from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.application.dto.aircraft import CreateAircraftDTO


@dataclass
class AircraftsLoaderResponse:
    invalid: int
    airports: list[CreateAircraftDTO]


class AircraftsLoader(ABC):
    @abstractmethod
    async def load(self) -> AircraftsLoaderResponse:
        ...
