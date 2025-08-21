from src.application.dto.ticket import TicketFullInfoDTO
from src.application.repositories.tickets_repository import (
    TicketReadRepositoryInterface,
)
from src.application.services.currency_converter import CurrencyConverter
from src.entities.tickets.filters import TicketsFilter


class FilterTickets:
    def __init__(self, repository: TicketReadRepositoryInterface, currency_converter: CurrencyConverter) -> None:
        self.repository = repository
        self.currency_converter = currency_converter

    async def __call__(self, filters: TicketsFilter) -> list[TicketFullInfoDTO]:
        tickets = await self.repository.filter(filters=filters)

        for ticket in tickets:
            if ticket.currency != "RUB":
                ticket.price = await self.currency_converter.to_rub(ticket.currency, ticket.price)
                ticket.currency = "RUB"

        return tickets
