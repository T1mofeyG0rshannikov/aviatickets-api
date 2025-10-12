import json
from zoneinfo import ZoneInfo

import airportsdata

from avia.application.services.timezone_resolver import TimezoneResolverInterface
from avia.entities.airport.value_objects.iata_code import IATACode
from redis import Redis # type: ignore


class TimezoneResolver(TimezoneResolverInterface):
    def __init__(self, redis: Redis) -> None:
        self._redis = redis
        self._cache_key = "airportsdata_cache_key"
        self._airportsdata = None

    def get_airports(self) -> dict:
        if self._airportsdata:
            return self._airportsdata

        cache = self._redis.get(self._cache_key)
        if cache is None:
            data = airportsdata.load("IATA")
            self._redis.set(self._cache_key, json.dumps(data))
            self._airportsdata = data
            return data

        data = json.loads(cache)
        self._airportsdata = data
        return data

    def get_timezone(self, iata: IATACode) -> ZoneInfo:
        airports = self.get_airports()
        airport = airports.get(iata)
        return ZoneInfo(airport["tz"])
