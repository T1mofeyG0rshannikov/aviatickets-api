from src.application.usecases.airports.import_airports.load_data import AirportLoadData
from src.application.usecases.airports.import_airports.loader import (
    AirportsLoader,
    AirportsLoaderResponse,
)


class AirportsCsvParser(AirportsLoader):
    def __init__(self, data: list[list[str]]) -> None:
        self._data = data

    def get_russian_name(self, keywords: str) -> str | None:
        try:
            return keywords.split(", ")[1]
        except:
            return None

    async def load(self) -> AirportsLoaderResponse:
        data = []
        invalid = 0

        for row in self._data:
            try:
                data.append(
                    AirportLoadData(
                        name=row[3],
                        continent=row[7],
                        country_iso=row[8],
                        region_iso=row[9],
                        municipality=row[10],
                        scheduled_service=row[11],
                        icao=row[12],
                        iata=row[13],
                        gps_code=row[14],
                        name_russian=self.get_russian_name(row[18]),
                    )
                )
            except (ValueError, KeyError):
                invalid += 1

        return AirportsLoaderResponse(airports=data, invalid=invalid)
