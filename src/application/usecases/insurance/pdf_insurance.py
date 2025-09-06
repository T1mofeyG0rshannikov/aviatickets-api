from dataclasses import dataclass
from uuid import UUID

from entities.insurance.insurance import Insurance
from src.application.services.file_manager import File


@dataclass(frozen=True)
class PdfInsuranceRecord:
    name: str
    content_path: str
    user_ticket_id: UUID


class PdfInsurance(File):
    @classmethod
    def from_insurance(cls, insurance: Insurance, content: bytes) -> "PdfInsurance":
        return cls(name=cls.get_name(insurance), content=content)

    @classmethod
    def get_name(self, insurance: Insurance) -> str:
        return insurance.contract
