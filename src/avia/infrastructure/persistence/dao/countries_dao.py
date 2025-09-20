from sqlalchemy import desc, func, or_, select
from sqlalchemy.orm import joinedload

from avia.application.dto.location import CountryWithAirportsDTO
from avia.application.persistence.dao.countries_dao import CountriesDAOInterface
from avia.infrastructure.persistence.db.models.models import AirportOrm, CountryOrm
from avia.infrastructure.persistence.persist_base import PersistenceBase


class CountriesDAO(PersistenceBase, CountriesDAOInterface):
    async def filter(self, start_with: str, limit=10) -> list[CountryWithAirportsDTO]:
        results = await self.db.execute(
            select(CountryOrm)
            .outerjoin(AirportOrm)
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
            .group_by(CountryOrm.id, CountryOrm.name, CountryOrm.name_english, CountryOrm.iso)
            .having(func.count(AirportOrm.id) > 0)
            .order_by(desc(func.count(AirportOrm.id)), CountryOrm.name)
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
