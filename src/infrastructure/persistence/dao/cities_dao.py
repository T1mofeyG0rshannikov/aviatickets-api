from sqlalchemy import or_, select
from sqlalchemy.orm import joinedload

from src.application.dto.location import CityWithAirportsDTO
from src.application.persistence.dao.cities_dao import CitiesDAOInterface
from src.infrastructure.persistence.db.models.models import CityOrm
from src.infrastructure.persistence.persist_base import PersistBase


class CitiestDAO(PersistBase, CitiesDAOInterface):
    async def filter(self, start_with: str, limit=10) -> list[CityWithAirportsDTO]:
        results = await self.db.execute(
            select(CityOrm)
            .options(
                joinedload(CityOrm.airports),
            )
            .where(
                or_(
                    CityOrm.name.istartswith(f"{start_with}"),
                    CityOrm.name_english.istartswith(f"{start_with}"),
                )
            )
            .limit(limit)
        )

        cities = results.scalars().unique().all()

        return [
            CityWithAirportsDTO(
                id=city.id, name=city.name, name_english=city.name_english, airports=[a.id for a in city.airports]
            )
            for city in cities
        ]
