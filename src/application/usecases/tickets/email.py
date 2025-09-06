from abc import ABC, abstractmethod

from src.application.services.file_manager import File
from src.application.usecases.tickets.pdf.get import GetPdfTicket
from src.entities.exceptions import AccessDeniedError
from src.entities.user.user import User
from src.entities.user_ticket.exceptions import UserTicketNotFoundError
from src.entities.user_ticket.user_ticket_repository import (
    UserTicketRepositoryInterface,
)
from src.entities.value_objects.entity_id import EntityId


class EmailSenderInterface(ABC):
    @abstractmethod
    def send(self, recipient_email: str, subject: str, body: str, files: list[File]) -> None:
        ...


class SendPdfTicketToEmail:
    def __init__(
        self,
        user_ticket_repository: UserTicketRepositoryInterface,
        email_sender: EmailSenderInterface,
        get_pdf_ticket: GetPdfTicket,
    ) -> None:
        self.email_sender = email_sender
        self.repository = user_ticket_repository
        self.get_pdf_ticket = get_pdf_ticket

    async def __call__(self, user_ticket_id: EntityId, user: User) -> None:
        user_ticket = await self.repository.get(id=user_ticket_id)
        if user_ticket is None:
            raise UserTicketNotFoundError(f"Нет пользовательского билета с id='{user_ticket_id}'")

        if user_ticket.user_id != user.id:
            raise AccessDeniedError("Вы можете получать на почту только свои билеты")

        file = await self.get_pdf_ticket(user_ticket_id=user_ticket_id, user=user)
        return self.email_sender.send(
            recipient_email=user.email, subject="Электронный билет", body="Вот ваш билет", files=[file]
        )
