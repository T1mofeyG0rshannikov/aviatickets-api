from sqlalchemy import or_, select
from sqlalchemy.orm import joinedload

from src.application.builders.airport import AirportFullInfoDTOBuilder
from src.application.dto.airports.full_info import AirportFullInfoDTO
from src.application.repositories.airport_read_repository import (
    AirportReadRepositoryInterface,
)
from src.infrastructure.db.models.models import (
    AirportOrm,
    CityOrm,
    CountryOrm,
    RegionOrm,
)
from src.infrastructure.repositories.base_repository import BaseRepository


class AirportReadRepository(BaseRepository, AirportReadRepositoryInterface):
    async def filter(self, start_with: str, limit=10) -> list[AirportFullInfoDTO]:
        results = await self.db.execute(
            select(AirportOrm)
            .join(AirportOrm.city)
            .join(AirportOrm.country)
            .join(AirportOrm.region)
            .options(
                joinedload(AirportOrm.city),
                joinedload(AirportOrm.country),
                joinedload(AirportOrm.region),
            )
            .where(
                or_(
                    CityOrm.name.istartswith(f"{start_with}"),
                    CityOrm.name_english.istartswith(f"{start_with}"),
                    RegionOrm.name.istartswith(f"{start_with}"),
                    RegionOrm.name_english.istartswith(f"{start_with}"),
                    RegionOrm.iso.istartswith(f"{start_with}"),
                    CountryOrm.name.istartswith(f"{start_with}"),
                    CountryOrm.name_english.istartswith(f"{start_with}"),
                    CountryOrm.iso.istartswith(f"{start_with}"),
                    AirportOrm.name.istartswith(f"{start_with}"),
                    AirportOrm.name_russian.istartswith(f"{start_with}"),
                    AirportOrm.iata.istartswith(f"{start_with}"),
                    AirportOrm.icao.istartswith(f"{start_with}"),
                )
            )
            .limit(limit)
        )

        airports = results.scalars().unique().all()

        return [AirportFullInfoDTOBuilder.from_orm(airport) for airport in airports]
