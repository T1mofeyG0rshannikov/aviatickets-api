from src.application.dto.bulk_result import BulkResult
from src.application.factories.airport_factory import AirportFactory
from src.application.persistence.etl_importers.airport_importer import (
    AirportBulkSaverInterface,
)
from src.application.persistence.transaction import Transaction
from src.application.usecases.airports.import_airports.load_data_to_create_dto_adapter import (
    ConvertAirportLoadDataToCreateData,
)
from src.application.usecases.airports.import_airports.loader import AirportsLoader
from src.entities.airport.airport import Airport
from src.entities.airport.airport_repository import AirportRepositoryInterface
from src.entities.airport.value_objects.iata_code import IATACode
from src.entities.exceptions import DomainError


class ImportAirports:
    def __init__(
        self,
        transaction: Transaction,
        repository: AirportRepositoryInterface,
        saver: AirportBulkSaverInterface,
        loader: AirportsLoader,
        converter: ConvertAirportLoadDataToCreateData,
    ) -> None:
        self.repository = repository
        self.saver = saver
        self.loader = loader
        self.transaction = transaction
        self.converter = converter

    async def get_exist_codes(self) -> set[IATACode]:
        airports = await self.repository.all()
        return {airport.iata for airport in airports}

    async def __call__(self) -> BulkResult:
        skipped = 0

        loader_response = await self.loader.load()

        airports = loader_response.airports
        invalid = loader_response.invalid

        adapter_response = await self.converter(airports=airports)

        create_airports_dto = adapter_response.airports
        invalid += adapter_response.invalid

        create_data: list[Airport] = []

        exist_codes = await self.get_exist_codes()

        for airport in create_airports_dto:
            print(airport.iata, exist_codes, airport.iata in exist_codes)
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

        await self.saver.add_many(create_data)
        await self.transaction.commit()
        return BulkResult(skipped=skipped, inserted=len(create_data), invalid=invalid)
