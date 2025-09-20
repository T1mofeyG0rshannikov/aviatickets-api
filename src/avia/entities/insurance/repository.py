from typing import Protocol

from avia.entities.insurance.insurance import Insurance
from avia.entities.value_objects.entity_id import EntityId


class InsuranceRepositoryInterface(Protocol):
    # async def get_by_user_ticket_id(self, user_ticket_id: EntityId) -> Insurance | None:
    #    raise NotImplementedError

    async def get(self, id: EntityId) -> Insurance | None:
        raise NotImplementedError

    async def save(self, insurance: Insurance) -> None:
        raise NotImplementedError
