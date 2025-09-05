from src.application.dao.ticket_dao import TicketDAOInterface
from src.application.dto.ticket import TicketFullInfoDTO
from src.application.services.currency_converter import CurrencyConverter
from src.entities.tickets.filters import TicketsFilter
from src.entities.value_objects.price.currency_enum import CurrencyEnum


class FilterTickets:
    def __init__(self, dao: TicketDAOInterface, currency_converter: CurrencyConverter) -> None:
        self.dao = dao
        self.currency_converter = currency_converter

    async def __call__(self, filters: TicketsFilter) -> list[TicketFullInfoDTO]:
        exchange_rates = await self.currency_converter.exchange_rate_service.get()

        tickets = await self.dao.filter(filters=filters, exchange_rates=exchange_rates)

        for ticket in tickets:
            if ticket.currency != CurrencyEnum.rub:
                ticket.price = await self.currency_converter.to_rub(ticket.currency, ticket.price)
                ticket.currency = CurrencyEnum.rub

        return tickets
