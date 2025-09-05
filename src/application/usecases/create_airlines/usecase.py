from src.application.etl_importers.airline_importer import AirlineImporterInterface
from src.application.factories.airline_factory import AirlineFactory
from src.application.usecases.create_airlines.loader import AirlinesLoader
from src.entities.airline.airline_repository import AirlineRepositoryInterface
from src.entities.airline.value_objects.iata_code import IATACode
from src.entities.exceptions import DomainError


class CreateAirlines:
    def __init__(
        self, repository: AirlineRepositoryInterface, importer: AirlineImporterInterface, loader: AirlinesLoader
    ) -> None:
        self.repository = repository
        self.loader = loader
        self.importer = importer

    async def get_exist_airlines_iatas(self) -> list[IATACode]:
        airlines = await self.repository.all()

        return [airline.iata for airline in airlines]

    async def __call__(self) -> None:
        parsed_data = self.loader.load()

        exist_data = await self.get_exist_airlines_iatas()

        data_to_create = []
        for data in parsed_data:
            if data.iata not in exist_data:
                try:
                    data_to_create.append(
                        AirlineFactory.create(
                            iata=data.iata, icao=data.icao, name=data.name, name_russian=data.name_russian
                        )
                    )
                except DomainError as e:
                    print(f"Error while building Airline: {e}")

        return await self.importer.add_many(airlines=data_to_create)  # type: ignore
