"""Value objects for Todo identifier."""

from dataclasses import dataclass
from uuid import UUID, uuid4


@dataclass(frozen=True)
class EntityId:
    """Value object representing the identifier of entity"""

    value: UUID

    @staticmethod
    def generate() -> "EntityId":
        """Generate a new ID"""
        return EntityId(uuid4())

    def __str__(self) -> str:
        return str(self.value)
