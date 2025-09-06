from src.application.dto.bulk_result import BulkResult
from src.application.factories.airport_factory import AirportFactory
from src.application.persistence.etl_importers.airport_importer import (
    AirportImporterInterface,
)
from src.application.usecases.airports.create.loader import AirportsLoader
from src.entities.airport.airport import Airport
from src.entities.airport.airport_repository import AirportRepositoryInterface
from src.entities.airport.value_objects.iata_code import IATACode
from src.entities.exceptions import DomainError
from src.entities.location.location_repository import LocationRepositoryInterface


class CreateAirports:
    def __init__(
        self,
        repository: AirportRepositoryInterface,
        importer: AirportImporterInterface,
        loader: AirportsLoader,
        location_repository: LocationRepositoryInterface,
    ) -> None:
        self.repository = repository
        self.location_repository = location_repository
        self.importer = importer
        self.loader = loader

    async def get_exist_codes(self) -> set[IATACode]:
        airports = await self.repository.all()
        return {airport.iata for airport in airports}

    async def __call__(self) -> BulkResult:
        skipped = 0

        loader_response = await self.loader.load()

        airports = loader_response.airports
        invalid = loader_response.invalid

        create_data: list[Airport] = []

        exist_codes = await self.get_exist_codes()

        for airport in airports:
            if airport.iata in exist_codes:
                skipped += 1
            else:
                try:
                    create_data.append(
                        AirportFactory.create(
                            name=airport.name,
                            continent=airport.continent,
                            country_id=airport.country_id,
                            region_id=airport.region_id,
                            city_id=airport.city_id,
                            scheduled_service=airport.scheduled_service,
                            icao=airport.icao,
                            iata=airport.iata,
                            gps_code=airport.gps_code,
                            name_russian=airport.name_russian,
                        )
                    )
                except DomainError as e:
                    invalid += 1
                    print(f"Error while building Airport: {e}")
                except DomainError:
                    continue

        inserted = await self.importer.add_many(airports=create_data)

        return BulkResult(skipped=skipped, inserted=inserted, invalid=invalid)
