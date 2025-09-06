from sqlalchemy import select

from src.application.persistence.data_mappers.ticket_files import (
    TicketFilesDataMapperInterface,
)
from src.application.usecases.tickets.pdf.pdf_ticket import PdfTicketRecord
from src.entities.value_objects.entity_id import EntityId
from src.infrastructure.persistence.dao.base_dao import BaseDAO
from src.infrastructure.persistence.db.models.models import PdfTicketOrm


class TicketFilesDataMapper(BaseDAO, TicketFilesDataMapperInterface):
    async def get_user_ticket_file(self, user_ticket_id: EntityId) -> PdfTicketRecord | None:
        result = await self.db.execute(select(PdfTicketOrm).where(PdfTicketOrm.user_ticket_id == user_ticket_id.value))

        pdf_ticket = result.scalar()

        return (
            PdfTicketRecord(
                name=pdf_ticket.name, content_path=pdf_ticket.content_path, user_ticket_id=pdf_ticket.user_ticket_id
            )
            if pdf_ticket
            else None
        )

    async def save(self, name: str, content_path: str, user_ticket_id: EntityId) -> None:
        self.db.add(PdfTicketOrm(name=name, content_path=content_path, user_ticket_id=user_ticket_id.value))

        await self.db.commit()
