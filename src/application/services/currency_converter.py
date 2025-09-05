from abc import ABC, abstractmethod
from decimal import Decimal

from src.entities.exceptions import InvalidCredentialsError
from src.entities.value_objects.price.currency_enum import CurrencyEnum


class ExchangeRateServiceInterface(ABC):
    @abstractmethod
    async def get(self) -> dict[str, Decimal]:
        ...


class CurrencyConverter:
    """
    A currency converter that uses an external service to get up-to-date exchange rates.

    Attributes:
        exchange_rate_service (ExchangeRateServiceInterface): The service providing the exchange rates.
    """

    def __init__(self, exchange_rate_service: ExchangeRateServiceInterface) -> None:
        self.exchange_rate_service = exchange_rate_service

    async def to_rub(self, currency: CurrencyEnum, value: Decimal) -> Decimal:
        exchange_rates = await self.exchange_rate_service.get()

        try:
            exchange_rate = exchange_rates[currency]
        except KeyError:
            raise InvalidCredentialsError(f"no currency rate - {currency}")

        return round(value * exchange_rate, 2)
