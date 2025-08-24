from zoneinfo import ZoneInfo

import airportsdata

from src.entities.airport.value_objects.iata_code import IATACode


class TimezoneResolver:
    def get_timezone(self, iata: IATACode) -> ZoneInfo:
        airports = airportsdata.load("IATA")
        airport = airports.get(iata)
        return ZoneInfo(airport["tz"])
