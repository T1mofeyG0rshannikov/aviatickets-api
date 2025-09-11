from abc import ABC, abstractmethod

from src.application.usecases.insurance.pdf_insurance import PdfInsuranceRecord
from src.entities.value_objects.entity_id import EntityId


class InsuranceFilesDataMapperInterface(ABC):
    @abstractmethod
    async def get_insurance_file(self, user_ticket_id: EntityId) -> PdfInsuranceRecord | None:
        ...

    @abstractmethod
    async def save(self, name: str, content_path: str, insurance_id: EntityId) -> None:
        ...
