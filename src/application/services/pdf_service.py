from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol

from src.application.dto.pdf_service import AdapterPdfField
from src.application.dto.user_ticket import UserTicketFullInfoDTO
from src.application.usecases.tickets.pdf.pdf_ticket import PdfTicket


@dataclass
class PdfFieldsAdapter:
    template_name: str
    data_fields_list: list[list[AdapterPdfField]]


class PdfTicketGeneratorStrategy(ABC):
    @abstractmethod
    async def execute(self, user_ticket: UserTicketFullInfoDTO) -> PdfTicket:
        ...


class PdfServiceInterface(Protocol):
    def set_file(self, file_path: str) -> None:
        raise NotImplementedError

    def update_form(self, adapter: list[AdapterPdfField]) -> None:
        raise NotImplementedError

    def save_file(self) -> bytes:
        raise NotImplementedError

    def merge_byte_files(self, files: list[bytes]) -> bytes:
        raise NotImplementedError
