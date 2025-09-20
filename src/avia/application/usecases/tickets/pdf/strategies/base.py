from abc import ABC, abstractmethod

from avia.application.dto.user_ticket import UserTicketFullInfoDTO
from avia.application.services.pdf_service import PdfFieldsAdapter


class PdfTicketAdapter(ABC):
    @abstractmethod
    async def execute(self, user_ticket: UserTicketFullInfoDTO) -> list[PdfFieldsAdapter]:
        ...
