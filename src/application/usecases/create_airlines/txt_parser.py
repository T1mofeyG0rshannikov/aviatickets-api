from src.entities.airline.dto import CreateAirlineDTO
from src.entities.airline.iata_code import IATACode
from src.entities.airline.icao_code import ICAOCode


class AirlinesTXTParser:
    def execute(self, input_data: list[str]) -> list[CreateAirlineDTO]:
        output_data = []

        for line in input_data:
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
                print(f"Error while building CreateAirlineDTO: {e}")

        return output_data
