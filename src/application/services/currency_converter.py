from abc import ABC, abstractmethod

from src.entities.exceptions import InvalidcredentialsError


class ExchangeRateServiceInterface(ABC):
    @abstractmethod
    async def get(self) -> dict[str, float]:
        ...


class CurrencyConverter:
    def __init__(self, exchange_rate_service: ExchangeRateServiceInterface) -> None:
        self.exchange_rate_service = exchange_rate_service

    async def to_rub(self, currency: str, value: str) -> float:
        exchange_rates = await self.exchange_rate_service.get()

        try:
            exchange_rate = exchange_rates[currency]
        except KeyError:
            raise InvalidcredentialsError(f"нет курса валюты - {currency}")

        return round(value * exchange_rate, 2)
