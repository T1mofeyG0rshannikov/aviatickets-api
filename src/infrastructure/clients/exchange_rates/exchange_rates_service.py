import json
from decimal import Decimal

import httpx
from redis import Redis  # type: ignore

from src.application.services.currency_converter import ExchangeRateServiceInterface
from src.infrastructure.clients.base_http_client import BaseHttpClient
from src.infrastructure.clients.exchange_rates.config import ExchangeRateServiceConfig
from src.infrastructure.clients.retry_decorator import retry
from src.infrastructure.exceptions import FetchAPIError


class ExchangeRateService(ExchangeRateServiceInterface, BaseHttpClient):
    def __init__(
        self,
        session: httpx.AsyncClient,
        config: ExchangeRateServiceConfig,
        redis: Redis,
        cache_key="exchange_rates",
        ttl=300,
    ) -> None:
        super().__init__(session)
        self._config = config
        self._redis = redis
        self._cache_key = cache_key
        self._ttl = ttl

    @retry()
    async def fetch(self) -> dict[str, Decimal]:
        response = await self.session.get(self._config.url)
        if response.is_error:
            raise FetchAPIError("cant parse currencies")

        data = response.json()

        exchange_rate = data["Valute"]

        result = {"RUB": Decimal(1)}

        for currency, currency_data in exchange_rate.items():
            result[currency] = Decimal(currency_data["Value"])

        return result

    async def get(self) -> dict[str, Decimal]:
        cache = self._redis.get(self._cache_key)
        if cache is None:
            data = await self.fetch()
            self._redis.set(self._cache_key, json.dumps(data))

            return data

        return json.loads(cache)
