from src.entities.airline.airline import Airline


class AirlinesTXTParser:
    def execute(self, input_data: list[str]) -> list[Airline]:
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
                    Airline.create(
                        iata=iata,
                        icao=icao,
                        name=name,
                        name_russian=name_russian,
                    )
                )
            except ValueError as e:
                print(f"Error while building Airline: {e}")

        return output_data
