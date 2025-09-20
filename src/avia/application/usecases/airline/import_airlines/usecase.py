from avia.application.factories.airline_factory import AirlineFactory
from avia.application.persistence.bulk_savers.airline_saver import (
    AirlineBulkSaverInterface,
)
from avia.application.persistence.transaction import Transaction
from avia.application.usecases.airline.import_airlines.loader import AirlinesLoader
from avia.entities.airline.airline_repository import AirlineRepositoryInterface
from avia.entities.exceptions import DomainError


class ImportAirlines:
    def __init__(
        self,
        repository: AirlineRepositoryInterface,
        importer: AirlineBulkSaverInterface,
        loader: AirlinesLoader,
        transaction: Transaction,
    ) -> None:
        self.repository = repository
        self.loader = loader
        self.importer = importer
        self.transaction = transaction

    async def __call__(self) -> None:
        parsed_data = self.loader.load()

        exist_iata_codes = await self.repository.all_iata_codes()

        data_to_create = []
        for data in parsed_data:
            if data.iata not in exist_iata_codes:
                try:
                    data_to_create.append(
                        AirlineFactory.create(
                            iata=data.iata, icao=data.icao, name=data.name, name_russian=data.name_russian
                        )
                    )
                except DomainError as e:
                    print(f"Error while building Airline: {e}")

        await self.importer.add_many(data_to_create)
        await self.transaction.commit()
