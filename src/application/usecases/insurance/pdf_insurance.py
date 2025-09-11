from dataclasses import dataclass
from uuid import UUID

from src.application.services.file_manager import File
from src.entities.insurance.insurance import Insurance


@dataclass(frozen=True)
class PdfInsuranceRecord:
    name: str
    content_path: str
    insurance_id: UUID


class PdfInsurance(File):
    @classmethod
    def from_insurance(cls, insurance: Insurance, content: bytes) -> "PdfInsurance":
        return cls(name=cls.get_name(insurance), content=content)

    @classmethod
    def get_name(self, insurance: Insurance) -> str:
        return insurance.contract.value.replace("/", "-") + ".pdf"
