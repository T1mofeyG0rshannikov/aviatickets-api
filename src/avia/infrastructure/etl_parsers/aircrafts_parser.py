from avia.application.dto.aircraft import CreateAircraftDTO
from avia.application.usecases.aircraft.import_aircrafts.loader import (
    AircraftsLoader,
    AircraftsLoaderResponse,
)


class AircraftCsvParser(AircraftsLoader):
    def __init__(self, data: list[list[str]]) -> None:
        self._data = data

    async def load(self) -> AircraftsLoaderResponse:
        data = []
        invalid = 0
        print(self._data)
        for row in self._data:
            print(row)
            try:
                data.append(CreateAircraftDTO(iata=row[0], name=row[2], wtc=row[3]))
            except (ValueError, KeyError, IndexError):
                invalid += 1

        return AircraftsLoaderResponse(airports=data, invalid=invalid)
