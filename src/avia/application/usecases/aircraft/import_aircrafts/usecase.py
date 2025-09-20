from avia.application.dto.bulk_result import BulkResult
from avia.application.factories.aircraft_factory import AircraftFactory
from avia.application.persistence.bulk_savers.aircraft_saver import (
    AircraftBulkSaverInterface,
)
from avia.application.persistence.transaction import Transaction
from avia.application.usecases.aircraft.import_aircrafts.loader import AircraftsLoader
from avia.entities.aircraft.entity import Aircraft
from avia.entities.aircraft.repository import AircraftRepositoryInterface
from avia.entities.exceptions import DomainError


class ImportAircrafts:
    def __init__(
        self,
        transaction: Transaction,
        repository: AircraftRepositoryInterface,
        saver: AircraftBulkSaverInterface,
        loader: AircraftsLoader,
    ) -> None:
        self.repository = repository
        self.saver = saver
        self.loader = loader
        self.transaction = transaction

    async def __call__(self) -> BulkResult:
        skipped = 0

        loader_response = await self.loader.load()

        aircrafts = loader_response.airports
        invalid = loader_response.invalid

        create_data: list[Aircraft] = []

        exist_codes = await self.repository.all_iata_codes()

        for aircraft in aircrafts:
            # print(airport.iata, exist_codes, airport.iata in exist_codes)
            if aircraft.iata in exist_codes:
                skipped += 1
            else:
                try:
                    create_data.append(AircraftFactory.create(name=aircraft.name, iata=aircraft.iata, wtc=aircraft.wtc))
                except DomainError as e:
                    invalid += 1
                    print(f"Error while building Airport: {e}")
                except DomainError:
                    continue

        await self.saver.add_many(create_data)
        await self.transaction.commit()
        return BulkResult(skipped=skipped, inserted=len(create_data), invalid=invalid)
