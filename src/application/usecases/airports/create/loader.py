from abc import ABC, abstractmethod

from src.application.dto.airports.create_dto import CreateAirportDTO

from dataclasses import dataclass


@dataclass
class AirportsLoaderResponse:
    invalid: int
    airports: list[CreateAirportDTO]


class AirportsLoader(ABC):
    @abstractmethod
    async def load(self) -> AirportsLoaderResponse:
        ...