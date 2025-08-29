from src.application.dto.airline import CreateAirlineDTO
from src.application.usecases.create_airlines.loader import AirlinesLoader


class AirlinesTXTParser(AirlinesLoader):
    def __init__(self, data: list[str]) -> None:
        self._data = data

    def load(self) -> list[CreateAirlineDTO]:
        output_data = []

        for line in self._data:
            try:
                iata, icao, name, name_russian = line.split("\t")
                name_russian = name_russian.strip()
            except (ValueError, IndexError) as e:
                print(f"Invalid .txt file content while loading aurlines: {e}")
                continue

            try:
                output_data.append(
                    CreateAirlineDTO(
                        iata=iata,
                        icao=icao,
                        name=name,
                        name_russian=name_russian,
                    )
                )
            except ValueError as e:
                print(f"Error while building Airline: {e}")

        return output_data
