from abc import ABC, abstractmethod

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
