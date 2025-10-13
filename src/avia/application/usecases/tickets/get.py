from avia.application.dto.ticket import TicketFullInfoDTO
from avia.application.persistence.dao.ticket_dao import TicketDAOInterface
from avia.application.services.currency_converter import CurrencyConverter
from avia.application.services.timezone_resolver import TimezoneResolverInterface
from avia.entities.tickets.exceptions import TicketNotFoundError
from avia.entities.value_objects.entity_id import EntityId
from avia.entities.value_objects.price.currency_enum import CurrencyEnum


class GetTicket:
    def __init__(
        self,
        ticket_dao: TicketDAOInterface,
        currency_converter: CurrencyConverter,
        timezone_resolver: TimezoneResolverInterface,
    ) -> None:
        self.dao = ticket_dao
        self.timezone_resolver = timezone_resolver
        self.currency_converter = currency_converter

    async def __call__(self, ticket_id: EntityId) -> TicketFullInfoDTO:
        ticket = await self.dao.get(ticket_id)

        if ticket is None:
            raise TicketNotFoundError(f"Нет билета с id='{ticket_id}'")

        if ticket.currency != CurrencyEnum.rub:
            ticket.price = await self.currency_converter.to_rub(ticket.currency, ticket.price)
            ticket.currency = CurrencyEnum.rub

        for itinerary in ticket.itineraries:
            for segment in itinerary.segments:
                departure_utc = segment.departure_at
                departure_tz = self.timezone_resolver.get_timezone(iata=segment.origin_airport.iata)
                departure_local_time = departure_utc.astimezone(departure_tz)

                segment.departure_at = departure_local_time

                return_utc = segment.return_at
                return_tz = self.timezone_resolver.get_timezone(iata=segment.destination_airport.iata)
                return_local_time = return_utc.astimezone(return_tz)
                segment.return_at = return_local_time

        return ticket
