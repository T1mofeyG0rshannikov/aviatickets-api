from avia.application.dto.location import CityWithAirportsDTO
from avia.application.persistence.dao.cities_dao import CitiesDAOInterface


class GetCities:
    def __init__(self, dao: CitiesDAOInterface) -> None:
        self.dao = dao

    async def __call__(self, start_with: str) -> list[CityWithAirportsDTO]:
        return await self.dao.filter(start_with)
