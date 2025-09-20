from sqlalchemy import select

from avia.application.persistence.data_mappers.insurance_files import (
    InsuranceFilesDataMapperInterface,
)
from avia.application.usecases.insurance.pdf_insurance import PdfInsuranceRecord
from avia.entities.value_objects.entity_id import EntityId
from avia.infrastructure.persistence.db.models.models import PdfInsuranceOrm
from avia.infrastructure.persistence.persist_base import PersistenceBase


class InsuranceFilesDataMapper(PersistenceBase, InsuranceFilesDataMapperInterface):
    async def get_insurance_file(self, insurance_id: EntityId) -> PdfInsuranceRecord | None:
        result = await self.db.execute(
            select(PdfInsuranceOrm).where(PdfInsuranceOrm.insurance_id == insurance_id.value)
        )

        pdf_insurance = result.scalar()

        return (
            PdfInsuranceRecord(
                name=pdf_insurance.name,
                content_path=pdf_insurance.content_path,
                insurance_id=pdf_insurance.insurance_id,
            )
            if pdf_insurance
            else None
        )

    async def save(self, name: str, content_path: str, insurance_id: EntityId) -> None:
        self.db.add(PdfInsuranceOrm(name=name, content_path=content_path, insurance_id=insurance_id.value))
