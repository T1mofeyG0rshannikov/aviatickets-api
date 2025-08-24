from abc import ABC, abstractmethod

from src.entities.exceptions import InvalidcredentialsError


class ExchangeRateServiceInterface(ABC):
    @abstractmethod
    async def get(self) -> dict[str, float]:
        ...


class CurrencyConverter:
    """
    A currency converter that uses an external service to get up-to-date exchange rates.

    Attributes:
        exchange_rate_service (ExchangeRateServiceInterface): The service providing the exchange rates.
    """

    def __init__(self, exchange_rate_service: ExchangeRateServiceInterface) -> None:
        self.exchange_rate_service = exchange_rate_service

    async def to_rub(self, currency: str, value: float) -> float:
        exchange_rates = await self.exchange_rate_service.get()

        try:
            exchange_rate = exchange_rates[currency]
        except KeyError:
            raise InvalidcredentialsError(f"нет курса валюты - {currency}")

        return round(value * exchange_rate, 2)
