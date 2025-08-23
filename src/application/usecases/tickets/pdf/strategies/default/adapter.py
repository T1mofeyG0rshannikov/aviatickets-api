from dataclasses import dataclass
from datetime import datetime, timedelta

from transliterate import translit

from src.application.dto.airports.full_info import AirportFullInfoDTO
from src.application.dto.ticket import TicketFullInfoDTO, TicketSegmentFullInfoDTO
from src.application.dto.user_ticket import AdapterPdfField, UserTicketFullInfoDTO
from src.application.services.currency_converter import CurrencyConverter
from src.application.usecases.tickets.pdf.strategies.base import PdfTicketAdapter
from src.application.usecases.tickets.pdf.strategies.default.config import (
    DefaultPdfTicketAdapterConfig,
)
from src.entities.location.city.city import City
from src.entities.location.country.country import Country
from src.entities.user_ticket.user_ticket import Passenger


@dataclass
class PdfFieldsAdapter:
    template_name: str
    data_fields_list: list[list[AdapterPdfField]]


class DefaultPdfTicketAdapter(PdfTicketAdapter):
    def __init__(self, config: DefaultPdfTicketAdapterConfig, currency_converter: CurrencyConverter) -> None:
        self.config = config
        self.currency_converter = currency_converter

    def get_flight_number(self, ticket: TicketSegmentFullInfoDTO) -> str:
        return f"{ticket.airline.iata}-{ticket.flight_number}"

    def get_place(self, city: City, country: Country) -> str:
        return f"{city.name_english.upper()}, {country.name_english.upper()}"

    def get_airport_place(self, airport: AirportFullInfoDTO) -> str:
        return self.get_place(airport.city, airport.country)

    def get_from_to(self, ticket: TicketFullInfoDTO) -> str:
        from_value = self.get_airport_place(ticket.segments[0].origin_airport)
        to_value = self.get_airport_place(ticket.segments[-1].destination_airport)
        return f"{from_value} - {to_value}"

    async def get_price(self, price: int, currency: str) -> str:
        price_in_rub = await self.currency_converter.to_rub(currency, price)
        return f"{price_in_rub:,.2f}"

    def format_date(self, date) -> str:
        return date.strftime("%A %d %B %Y").upper()

    def get_passengers(self, passengers: list[Passenger]) -> str:
        result = ""
        for passenger in passengers:
            first_name = translit(passenger.first_name, "ru", reversed=True).upper()
            second_name = translit(passenger.second_name, "ru", reversed=True).upper()

            result += f"{first_name}/{second_name}\n"

        return result

    def get_arriving_time(self, ticket: TicketFullInfoDTO) -> datetime:
        return ticket.departure_at + timedelta(minutes=ticket.duration)

    def get_origin_arriving_date(self, ticket: TicketFullInfoDTO) -> str:
        return self.get_arriving_time(ticket).strftime("%d %b %Y")

    def get_origin_arriving_time(self, ticket: TicketFullInfoDTO) -> str:
        return self.get_arriving_time(ticket).strftime("%H:%M")

    async def execute(self, user_ticket: UserTicketFullInfoDTO) -> list[PdfFieldsAdapter]:
        fields = []

        nav_fields = [
            AdapterPdfField(name="reservationCode", value="Not Available"),
            AdapterPdfField(
                name="originDateShort", value=user_ticket.ticket.segments[0].departure_at.strftime("%d-%m-%Y")
            ),
            AdapterPdfField(
                name="destinationDateShort", value=user_ticket.ticket.segments[-1].departure_at.strftime("%d-%m-%Y")
            ),
            AdapterPdfField(name="fromTo", value=self.get_from_to(user_ticket.ticket)),
            AdapterPdfField(name="currency", value="RUB"),
            AdapterPdfField(
                name="price", value=await self.get_price(user_ticket.ticket.price, user_ticket.ticket.currency)
            ),
            AdapterPdfField(name="passengers", value=self.get_passengers(user_ticket.passengers)),
        ]

        fields.append(PdfFieldsAdapter(template_name=self.config.nav_path, data_fields_list=[nav_fields]))

        tickets_fields = []

        for ticket in user_ticket.ticket.segments:
            ticket_fields = [
                AdapterPdfField(name="originFlight", value=self.get_flight_number(ticket)),
                AdapterPdfField(name="originDepartingTime", value=ticket.departure_at.strftime("%H:%M").upper()),
                AdapterPdfField(name="originDepartingDate", value=ticket.departure_at.strftime("%d %B %Y").upper()),
                AdapterPdfField(name="originArrivingDate", value=self.get_origin_arriving_date(ticket)),
                AdapterPdfField(name="originArrivingTime", value=self.get_origin_arriving_time(ticket)),
                AdapterPdfField(name="Text-AUYa372fuH", value=self.format_date(ticket.return_at)),
                AdapterPdfField(name="originDate", value=self.format_date(ticket.departure_at)),
                AdapterPdfField(name="originAirline", value=ticket.airline.name),
                AdapterPdfField(name="originStatus", value=ticket.status),
                AdapterPdfField(name="originClass", value=ticket.seat_class),
                AdapterPdfField(name="originAirportAddress", value=self.get_airport_place(ticket.origin_airport)),
                AdapterPdfField(name="originAirport", value=ticket.origin_airport.iata),
                AdapterPdfField(name="destinationAirport", value=ticket.destination_airport.iata),
                AdapterPdfField(
                    name="destinationAirportAddress", value=self.get_airport_place(ticket.destination_airport)
                ),
                AdapterPdfField(name="passengers", value=self.get_passengers(user_ticket.passengers)),
            ]

            tickets_fields.append(ticket_fields)

        fields.append(PdfFieldsAdapter(template_name=self.config.single_ticket_path, data_fields_list=tickets_fields))

        fields.append(PdfFieldsAdapter(template_name=self.config.bottom_path, data_fields_list=[]))

        return fields
