from src.application.dto.airports.full_info import AirportFullInfoDTO
from src.application.repositories.airport_read_repository import (
    AirportReadRepositoryInterface,
)


class GetAirports:
    def __init__(self, airport_read_repository: AirportReadRepositoryInterface) -> None:
        self.repository = airport_read_repository

    async def __call__(self, start_with: str) -> list[AirportFullInfoDTO]:
        return await self.repository.filter(start_with=start_with)
