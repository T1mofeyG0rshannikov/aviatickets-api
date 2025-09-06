import random
import string
from dataclasses import dataclass


@dataclass(frozen=True)
class InsuranceContract:
    """
    Value Object for insurance contract
    """

    value: str

    @classmethod
    def generate(cls) -> "InsuranceContract":
        part1 = "".join(random.choices(string.digits, k=7))

        part2 = "".join(random.choices(string.digits, k=7))

        part3 = "".join(random.choices(string.digits, k=2))

        part4 = "".join(random.choices(string.ascii_uppercase, k=2))

        result = f"{part1}-{part2}/{part3}{part4}"

        return cls(value=result)
