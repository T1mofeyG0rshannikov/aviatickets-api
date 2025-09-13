from sqlalchemy import or_, select
from sqlalchemy.orm import joinedload

from src.application.dto.location import CountryWithAirportsDTO
from src.application.persistence.dao.countries_dao import CountriesDAOInterface
from src.infrastructure.persistence.db.models.models import CountryOrm
from src.infrastructure.persistence.persist_base import PersistBase


class CountriesDAO(PersistBase, CountriesDAOInterface):
    async def filter(self, start_with: str, limit=10) -> list[CountryWithAirportsDTO]:
        results = await self.db.execute(
            select(CountryOrm)
            .options(
                joinedload(CountryOrm.airports),
            )
            .where(
                or_(
                    CountryOrm.name.istartswith(f"{start_with}"),
                    CountryOrm.name_english.istartswith(f"{start_with}"),
                    CountryOrm.iso.istartswith(f"{start_with}"),
                )
            )
            .limit(limit)
        )

        countries = results.scalars().unique().all()

        return [
            CountryWithAirportsDTO(
                id=country.id,
                iso=country.iso,
                name=country.name,
                name_english=country.name_english,
                airports=[a.id for a in country.airports],
            )
            for country in countries
        ]
