from datetime import datetime

from avia.application.dto.ticket import ListTicketDTO
from avia.application.persistence.dao.ticket_dao import TicketDAOInterface
from avia.application.services.currency_converter import CurrencyConverter
from avia.application.services.timezone_resolver import TimezoneResolverInterface
from avia.entities.tickets.filters import TicketsFilter
from avia.entities.value_objects.price.currency_enum import CurrencyEnum


class FilterTickets:
    def __init__(
        self,
        dao: TicketDAOInterface,
        timezone_resolver: TimezoneResolverInterface,
        currency_converter: CurrencyConverter,
    ) -> None:
        self.dao = dao
        self.currency_converter = currency_converter
        self.timezone_resolver = timezone_resolver

    def datetime_to_total_minutes(self, dt: datetime) -> int:
        hours = dt.hour
        minutes = dt.minute
        total_minutes = (hours * 60) + minutes
        return total_minutes

    async def __call__(self, filters: TicketsFilter) -> list[ListTicketDTO]:
        exchange_rates = await self.currency_converter.exchange_rate_service.get()

        tickets = await self.dao.filter(filters=filters, exchange_rates=exchange_rates)
        for ticket in tickets:
            if ticket.currency != CurrencyEnum.rub:
                ticket.price = await self.currency_converter.to_rub(ticket.currency, ticket.price)
                ticket.currency = CurrencyEnum.rub

            for itinerary in ticket.itineraries:
                departure_utc = itinerary.departure_at
                departure_tz = self.timezone_resolver.get_timezone(iata=itinerary.origin_airport.iata)
                departure_local_time = departure_utc.astimezone(departure_tz)

                itinerary.departure_at = departure_local_time

                return_utc = itinerary.return_at
                return_tz = self.timezone_resolver.get_timezone(iata=itinerary.destination_airport.iata)
                return_local_time = return_utc.astimezone(return_tz)
                itinerary.return_at = return_local_time

        tickets = filter(
            lambda t: filters.departure_at_time_min
            <= self.datetime_to_total_minutes(t.itineraries[0].departure_at)
            <= filters.departure_at_time_max
            and filters.return_at_time_min
            <= self.datetime_to_total_minutes(t.itineraries[-1].return_at)
            <= filters.return_at_time_max,
            tickets,
        )

        return tickets
