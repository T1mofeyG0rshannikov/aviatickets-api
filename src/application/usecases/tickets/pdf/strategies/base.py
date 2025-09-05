from abc import ABC, abstractmethod

from src.application.dto.user_ticket import UserTicketFullInfoDTO
from src.application.services.pdf_service import PdfFieldsAdapter


class PdfTicketAdapter(ABC):
    @abstractmethod
    async def execute(self, user_ticket: UserTicketFullInfoDTO) -> list[PdfFieldsAdapter]:
        ...
