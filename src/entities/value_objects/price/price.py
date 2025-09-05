from dataclasses import dataclass
from decimal import Decimal

from src.entities.value_objects.price.currency_enum import CurrencyEnum


@dataclass(frozen=True)
class Price:
    """Value Object for price field"""

    value: Decimal
    currency: CurrencyEnum
