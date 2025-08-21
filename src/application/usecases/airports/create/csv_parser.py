from src.application.dto.airports.csv_data import CsvAirportData


class AirportsCsvParser:
    def get_russian_name(self, keywords: str) -> str:
        try:
            return keywords.split(", ")[1]
        except:
            return None

    def execute(self, input_data: list[list[str]]) -> list[CsvAirportData]:
        return [
            CsvAirportData(
                name=row[3],
                continent=row[7],
                iso_country=row[8],
                iso_region=row[9],
                municipality=row[10],
                scheduled_service=row[11],
                icao=row[12],
                iata=row[13],
                gps_code=row[14],
                name_russian=self.get_russian_name(row[18]),
            )
            for row in input_data
        ]
