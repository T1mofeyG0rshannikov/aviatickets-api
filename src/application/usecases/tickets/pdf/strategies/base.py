from abc import ABC, abstractmethod
from typing import Protocol

from src.application.dto.user_ticket import AdapterPdfField, UserTicketFullInfoDTO
from src.interface_adapters.file import File


class PdfTicketAdapter(ABC):
    @abstractmethod
    def execute(self, user_ticket: UserTicketFullInfoDTO) -> list[AdapterPdfField]:
        ...


class PdfTicketGeneratorStrategy(ABC):
    @abstractmethod
    def execute(self, user_ticket: UserTicketFullInfoDTO) -> File:
        ...


class PdfServiceInterface(Protocol):
    def set_file(self, file_path: str) -> None:
        raise NotImplementedError

    def update_form(self, adapter: list[AdapterPdfField]) -> None:
        raise NotImplementedError

    def save_file(self) -> bytes:
        raise NotImplementedError

    def merge_byte_files(self) -> bytes:
        raise NotImplementedError
