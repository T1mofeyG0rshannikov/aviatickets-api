from typing import Protocol

from src.application.dto.airports.full_info import AirportFullInfoDTO


class AirportDAOInterface(Protocol):
    async def filter(self, start_with: str, limit: int) -> list[AirportFullInfoDTO]:
        raise NotImplementedError
