from src.application.usecases.create_airlines.txt_parser import AirlinesTXTParser
from src.entities.airline.dto import CreateAirlineDTO
from src.infrastructure.repositories.airlline_repository import AirlineRepository


class CreateAirlines:
    def __init__(self, repository: AirlineRepository, txt_parser: AirlinesTXTParser) -> None:
        self.repository = repository
        self.txt_parser = txt_parser

    async def get_exist_airlines_as_create_dto(self) -> list[CreateAirlineDTO]:
        airlines = await self.repository.all()

        return {
            CreateAirlineDTO(iata=airline.iata, icao=airline.icao, name=airline.name, name_russian=airline.name_russian)
            for airline in airlines
        }

    async def __call__(self, airlines: list[str]) -> None:
        parsed_data = self.txt_parser.execute(airlines)

        exist_data = await self.get_exist_airlines_as_create_dto()

        data_to_create = [data for data in parsed_data if data not in exist_data]

        return await self.repository.create_many(airlines=data_to_create)
