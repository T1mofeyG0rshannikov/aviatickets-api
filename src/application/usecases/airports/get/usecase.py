from src.application.dto.airports.full_info import AirportFullInfoDTO
from src.application.persistence.dao.airport_dao import AirportDAOInterface


class GetAirports:
    def __init__(self, airport_dao: AirportDAOInterface) -> None:
        self.dao = airport_dao

    async def __call__(self, start_with: str) -> list[AirportFullInfoDTO]:
        return await self.dao.filter(start_with=start_with)
