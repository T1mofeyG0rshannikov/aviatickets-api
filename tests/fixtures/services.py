import httpx
import pytest
from redis import Redis

from src.application.services.currency_converter import CurrencyConverter
from src.infrastructure.clients.exchange_rates.config import ExchangeRateServiceConfig
from src.infrastructure.clients.exchange_rates.exchange_rates_service import (
    ExchangeRateService,
)


@pytest.fixture
def exchange_rate_service_config() -> ExchangeRateServiceConfig:
    return ExchangeRateServiceConfig()


@pytest.fixture
def exchange_rate_service(
    session: httpx.AsyncClient,
    redis: Redis,
    exchange_rate_service_config: ExchangeRateServiceConfig,
) -> ExchangeRateService:
    return ExchangeRateService(
        session=session, redis=redis, config=exchange_rate_service_config, cache_key="exchange_rates", ttl=300
    )


@pytest.fixture
async def currency_converter(exchange_rate_service: ExchangeRateService) -> CurrencyConverter:
    return CurrencyConverter(exchange_rate_service)
