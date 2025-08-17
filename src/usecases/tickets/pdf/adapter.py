from datetime import datetime, timedelta
from typing import List

from transliterate import translit

from src.dto.airport import AirportFullInfoDTO
from src.entities.city import City
from src.entities.country.country import Country
from src.entities.user_ticket.user_ticket import Passenger
from src.usecases.tickets.filter.dto import TicketFullInfoDTO
from src.usecases.tickets.pdf.dto import AdapterPdfField, UserTicketFullInfoDTO


class PdfTicketAdapter:
    def get_place(self, city: City, country: Country) -> str:
        return f"{city.name_english.upper()}, {country.name_english.upper()}"

    def get_airport_place(self, airport: AirportFullInfoDTO) -> str:
        return self.get_place(airport.city, airport.country)

    def get_from_to(self, ticket: TicketFullInfoDTO) -> str:
        from_value = self.get_airport_place(ticket.origin_airport)
        to_value = self.get_airport_place(ticket.destination_airport)
        return f"{from_value} - {to_value}"

    def get_price(self, price: int) -> str:
        return f"{price:,.2f}"

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

    def execute(self, user_ticket: UserTicketFullInfoDTO) -> list[AdapterPdfField]:
        ticket = user_ticket.ticket
        """
        destinationDepartingDate
        destinationArrivingDate
        destinationDepartingTime
        destinationArrivingTime
        destinationAirline
        destinationClass
        destinationStatus
        destinationFlight
        originFlight
        reservationCode
        """
        return [
            AdapterPdfField(name="originDepartingTime", value=ticket.departure_at.strftime("%H:%M").upper()),
            AdapterPdfField(name="originDepartingDate", value=ticket.departure_at.strftime("%d %B %Y").upper()),
            AdapterPdfField(name="originArrivingDate", value=self.get_origin_arriving_date(ticket)),
            AdapterPdfField(name="originArrivingTime", value=self.get_origin_arriving_time(ticket)),
            AdapterPdfField(name="Text-AUYa372fuH", value=self.format_date(ticket.return_at)),
            AdapterPdfField(name="originDate", value=self.format_date(ticket.departure_at)),
            AdapterPdfField(name="originAirline", value=ticket.airline.name),
            AdapterPdfField(name="originDateShort", value=ticket.departure_at.strftime("%d-%m-%Y")),
            AdapterPdfField(name="destinationDateShort", value=ticket.return_at.strftime("%d-%m-%Y")),
            AdapterPdfField(name="originStatus", value="confirmed"),
            AdapterPdfField(name="originClass", value="economy"),
            AdapterPdfField(name="originAirportAddress", value=self.get_airport_place(ticket.origin_airport)),
            AdapterPdfField(name="originAirport", value=ticket.origin_airport.iata),
            AdapterPdfField(name="destinationAirport", value=ticket.destination_airport.iata),
            AdapterPdfField(name="destinationAirportAddress", value=self.get_airport_place(ticket.destination_airport)),
            AdapterPdfField(name="fromTo", value=self.get_from_to(ticket)),
            AdapterPdfField(name="currency", value="RUB"),
            AdapterPdfField(name="price", value=self.get_price(ticket.price)),
            AdapterPdfField(name="passengers", value=self.get_passengers(user_ticket.passengers)),
        ]
