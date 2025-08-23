from src.application.dao.airport_dao import AirportDAOInterface
from src.application.dto.airports.full_info import AirportFullInfoDTO


class GetAirports:
    def __init__(self, airport_dao: AirportDAOInterface) -> None:
        self.dao = airport_dao

    async def __call__(self, start_with: str) -> list[AirportFullInfoDTO]:
        return await self.dao.filter(start_with=start_with)
