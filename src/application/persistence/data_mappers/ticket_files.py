from abc import ABC, abstractmethod

from src.application.usecases.tickets.pdf.pdf_ticket import PdfTicketRecord
from src.entities.value_objects.entity_id import EntityId


class TicketFilesDataMapperInterface(ABC):
    @abstractmethod
    async def get_user_ticket_file(self, user_ticket_id: EntityId) -> PdfTicketRecord | None:
        ...

    @abstractmethod
    async def save(self, name: str, content_path: str, user_ticket_id: EntityId) -> None:
        ...
