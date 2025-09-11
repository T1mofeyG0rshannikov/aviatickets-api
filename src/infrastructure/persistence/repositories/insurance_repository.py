from sqlalchemy import select

from src.entities.insurance.insurance import Insurance
from src.entities.insurance.repository import InsuranceRepositoryInterface
from src.entities.value_objects.entity_id import EntityId
from src.infrastructure.persistence.db.models.models import InsuranceOrm
from src.infrastructure.persistence.persist_base import PersistBase
from src.infrastructure.persistence.repositories.mappers.insurance import (
    orm_to_insurance,
)


class InsuranceRepository(PersistBase, InsuranceRepositoryInterface):
    # async def get_by_user_ticket_id(self, user_ticket_id: EntityId) -> Insurance | None:
    #    result = await self.db.execute(select(InsuranceOrm).where(InsuranceOrm.user_ticket_id==id.value))
    #    insurance = result.scalar()
    #    return orm_to_insurance(insurance) if insurance else None

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
