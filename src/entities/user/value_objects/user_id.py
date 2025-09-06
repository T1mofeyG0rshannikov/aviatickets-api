from dataclasses import dataclass
from typing import Any
from uuid import UUID, uuid4

from src.entities.value_objects.entity_id import EntityId


@dataclass(frozen=True)
class UserId:
    """Id for user entity"""

    value: UUID

    @staticmethod
    def generate() -> "UserId":
        """Generate a new ID"""
        return UserId(uuid4())

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, UserId):
            raise NotImplementedError

        return self.value == other.value

    def __str__(self) -> str:
        return str(self.value)
