from src.application.dto.location import CountryWithAirportsDTO
from src.application.persistence.dao.countries_dao import CountriesDAOInterface


class GetCountries:
    def __init__(self, dao: CountriesDAOInterface) -> None:
        self.dao = dao

    async def __call__(self, start_with: str) -> list[CountryWithAirportsDTO]:
        return await self.dao.filter(start_with)
