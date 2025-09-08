from abc import ABC, abstractmethod
from dataclasses import dataclass

from src.application.usecases.airports.import_airports.load_data import AirportLoadData


@dataclass
class AirportsLoaderResponse:
    invalid: int
    airports: list[AirportLoadData]


class AirportsLoader(ABC):
    @abstractmethod
    async def load(self) -> AirportsLoaderResponse:
        ...
