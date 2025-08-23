from src.application.usecases.create_airlines.txt_parser import AirlinesTXTParser
from src.entities.airline.airlline_repository import AirlineRepositoryInterface
from src.entities.airline.iata_code import IATACode


class CreateAirlines:
    def __init__(self, repository: AirlineRepositoryInterface, txt_parser: AirlinesTXTParser) -> None:
        self.repository = repository
        self.txt_parser = txt_parser

    async def get_exist_airlines_iatas(self) -> list[IATACode]:
        airlines = await self.repository.all()

        return [airline.iata for airline in airlines]

    async def __call__(self, airlines: list[str]) -> None:
        parsed_data = self.txt_parser.execute(airlines)

        exist_data = await self.get_exist_airlines_iatas()

        data_to_create = [data for data in parsed_data if data.iata not in exist_data]

        return await self.repository.save_many(airlines=data_to_create)
