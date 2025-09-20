from sqlalchemy import select

from avia.entities.insurance.insurance import Insurance
from avia.entities.insurance.repository import InsuranceRepositoryInterface
from avia.entities.value_objects.entity_id import EntityId
from avia.infrastructure.persistence.db.models.models import InsuranceOrm
from avia.infrastructure.persistence.persist_base import PersistenceBase
from avia.infrastructure.persistence.repositories.mappers.insurance import (
    orm_to_insurance,
)


class InsuranceRepository(PersistenceBase, InsuranceRepositoryInterface):
    async def get(self, id: EntityId) -> Insurance | None:
        result = await self.db.execute(select(InsuranceOrm).where(InsuranceOrm.id == id.value))
        insurance = result.scalar()
        return orm_to_insurance(insurance) if insurance else None

    async def save(self, insurance: Insurance) -> None:
        self.db.add(
            InsuranceOrm(
                id=insurance.id.value,
                contract=insurance.contract.value,
                insured_id=insurance.insured_id.value,
                premium_value=insurance.premium.value,
                premium_currency=insurance.premium.currency,
                created_at=insurance.created_at,
                start_date=insurance.start_date,
                end_date=insurance.end_date,
                territory=insurance.territory,
            )
        )
