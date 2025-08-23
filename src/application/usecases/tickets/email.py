from abc import ABC, abstractmethod
from uuid import UUID

from src.application.usecases.tickets.pdf.usecase import CreatePdfTicket
from src.entities.exceptions import AccessDeniedError
from src.entities.user.user import User
from src.entities.user_ticket.exceptions import UserTicketNotFoundError
from src.entities.user_ticket.user_ticket_repository import (
    UserTicketRepositoryInterface,
)
from src.interface_adapters.file import File


class EmailSenderInterface(ABC):
    @abstractmethod
    def send(self, recipient_email: str, subject: str, body: str, files: list[File]) -> None:
        ...


class SendPdfTicketToEmail:
    def __init__(
        self,
        user_ticket_repository: UserTicketRepositoryInterface,
        create_pdf_ticket: CreatePdfTicket,
        email_sender: EmailSenderInterface,
    ) -> None:
        self.create_pdf_ticket = create_pdf_ticket
        self.email_sender = email_sender
        self.repository = user_ticket_repository

    async def __call__(self, user_ticket_id: UUID, user: User) -> None:
        user_ticket = await self.repository.get(id=user_ticket_id)
        if user_ticket is None:
            raise UserTicketNotFoundError(f"Нет пользовательского билета с id='{user_ticket_id}'")

        if user_ticket.user_id != user.id:
            raise AccessDeniedError("Вы можете получать на почту только свои билеты")

        file = await self.create_pdf_ticket(user_ticket_id=user_ticket_id, user=user)
        self.email_sender.send(
            recipient_email=user.email, subject="Электронный билет", body="Вот ваш билет", files=[file]
        )
