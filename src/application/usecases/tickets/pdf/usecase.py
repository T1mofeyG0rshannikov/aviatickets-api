from src.application.builders.user_ticket import UserTicketFullInfoAssembler
from src.application.usecases.tickets.pdf.strategies.base import (
    PdfTicketGeneratorStrategy,
)
from src.entities.exceptions import AccessDeniedError
from src.entities.user.user import User
from src.entities.user_ticket.exceptions import UserTicketNotFoundError
from src.entities.user_ticket.user_ticket_repository import (
    UserTicketRepositoryInterface,
)
from src.entities.value_objects.entity_id import EntityId
from src.interface_adapters.file import File
from src.interface_adapters.pdf_templates import PdfTemplatesEnum


class CreatePdfTicket:
    def __init__(
        self,
        user_ticket_repository: UserTicketRepositoryInterface,
        builder: UserTicketFullInfoAssembler,
        strategies: dict[PdfTemplatesEnum, PdfTicketGeneratorStrategy],
    ) -> None:
        self.user_ticket_repository = user_ticket_repository
        self.builder = builder
        self._strategies = strategies

    async def __call__(
        self, user_ticket_id: EntityId, user: User, template: PdfTemplatesEnum = PdfTemplatesEnum.default
    ) -> File:
        user_ticket = await self.user_ticket_repository.get(user_ticket_id)

        if user_ticket is None:
            raise UserTicketNotFoundError(f"Нет пользовательского билета с id='{user_ticket_id}'")

        if user_ticket.user_id != user.id:
            raise AccessDeniedError("Вы можете генерировать только свои билеты в pdf")

        user_ticket_dto = await self.builder.execute(user_ticket)

        return await self._strategies[template].execute(user_ticket_dto)
