import datetime

import pytest

from src.application.dto.airports.full_info import AirportFullInfoDTO
from src.application.dto.ticket import TicketFullInfoDTO, TicketSegmentFullInfoDTO
from src.application.services.currency_converter import CurrencyConverter
from src.application.usecases.tickets.filter import FilterTickets
from src.entities.airline.airline import Airline
from src.entities.city.city import City
from src.entities.country.country import Country
from src.entities.region.region import Region
from src.entities.tickets.filters import TicketsFilter
from src.infrastructure.repositories.tickets_read_repository import TicketReadRepository


@pytest.fixture
async def filter_tickets(
    ticket_read_repository: TicketReadRepository, currency_converter: CurrencyConverter
) -> FilterTickets:
    return FilterTickets(ticket_read_repository, currency_converter)


@pytest.mark.asyncio
async def test_call_returns_filtered_tickets(filter_tickets: FilterTickets, populate_db):
    filters = TicketsFilter(
        price_min=42000,
        price_max=50000,
        airline_ids=[499],
        origin_airport_ids=[78233, 51072],
        destination_airport_ids=[51072, 78233],
        duration_min=500,
        duration_max=2000,
        transfers=2,
        # departure_at=datetime.datetime(year=2024, month=9, day=18),
        # return_at=datetime.datetime(year=2026, month=9, day=18),
    )
    result = await filter_tickets(filters)
    expected_result = [
        TicketFullInfoDTO(
            id=197,
            duration=1165,
            price=42946.0,
            currency="RUB",
            transfers=2,
            segments=[
                TicketSegmentFullInfoDTO(
                    id=162,
                    flight_number="205",
                    destination_airport=AirportFullInfoDTO(
                        id=51072,
                        name="Dubai International Airport",
                        continent="AS",
                        country=Country(id=233, iso="AE", name="Объединенные Арабские Эмираты", name_english="UAE"),
                        region=None,
                        city=City(id=930, name="Дубай", name_english="Dubai"),
                        scheduled_service="yes",
                        icao="OMDB",
                        iata="DXB",
                        gps_code="OMDB",
                        name_russian=None,
                    ),
                    origin_airport=AirportFullInfoDTO(
                        id=78233,
                        name="Sheremetyevo International Airport",
                        continent="EU",
                        country=Country(id=183, iso="RU", name="Россия", name_english="Russia"),
                        region=Region(
                            id=111, iso="RU-MOS", name="Московская область", name_english="Moskovskaya oblast"
                        ),
                        city=City(id=2342, name="Москва", name_english="Moscow"),
                        scheduled_service="yes",
                        icao="UUEE",
                        iata="SVO",
                        gps_code="UUEE",
                        name_russian="Международный аэропорт Шереметьево",
                    ),
                    airline=Airline(
                        id=379, iata="N4", icao="NWS", name="Nordwind Airlines", name_russian="Nordwind Airlines"
                    ),
                    departure_at=datetime.datetime(2025, 8, 31, 18, 15, tzinfo=datetime.timezone.utc),
                    return_at=datetime.datetime(2025, 9, 1, 15, 50, tzinfo=datetime.timezone.utc),
                    duration=1165,
                    status="confirmed",
                    seat_class="economy",
                )
            ],
        ),
        TicketFullInfoDTO(
            id=198,
            duration=1165,
            price=42946.0,
            currency="RUB",
            transfers=2,
            segments=[
                TicketSegmentFullInfoDTO(
                    id=163,
                    flight_number="205",
                    destination_airport=AirportFullInfoDTO(
                        id=51072,
                        name="Dubai International Airport",
                        continent="AS",
                        country=Country(id=233, iso="AE", name="Объединенные Арабские Эмираты", name_english="UAE"),
                        region=None,
                        city=City(id=930, name="Дубай", name_english="Dubai"),
                        scheduled_service="yes",
                        icao="OMDB",
                        iata="DXB",
                        gps_code="OMDB",
                        name_russian=None,
                    ),
                    origin_airport=AirportFullInfoDTO(
                        id=78233,
                        name="Sheremetyevo International Airport",
                        continent="EU",
                        country=Country(id=183, iso="RU", name="Россия", name_english="Russia"),
                        region=Region(
                            id=111, iso="RU-MOS", name="Московская область", name_english="Moskovskaya oblast"
                        ),
                        city=City(id=2342, name="Москва", name_english="Moscow"),
                        scheduled_service="yes",
                        icao="UUEE",
                        iata="SVO",
                        gps_code="UUEE",
                        name_russian="Международный аэропорт Шереметьево",
                    ),
                    airline=Airline(
                        id=379, iata="N4", icao="NWS", name="Nordwind Airlines", name_russian="Nordwind Airlines"
                    ),
                    departure_at=datetime.datetime(2025, 8, 31, 18, 15, tzinfo=datetime.timezone.utc),
                    return_at=datetime.datetime(2025, 9, 14, 15, 50, tzinfo=datetime.timezone.utc),
                    duration=1165,
                    status="confirmed",
                    seat_class="economy",
                )
            ],
        ),
        TicketFullInfoDTO(
            id=199,
            duration=1165,
            price=42948.0,
            currency="RUB",
            transfers=2,
            segments=[
                TicketSegmentFullInfoDTO(
                    id=164,
                    flight_number="205",
                    destination_airport=AirportFullInfoDTO(
                        id=51072,
                        name="Dubai International Airport",
                        continent="AS",
                        country=Country(id=233, iso="AE", name="Объединенные Арабские Эмираты", name_english="UAE"),
                        region=None,
                        city=City(id=930, name="Дубай", name_english="Dubai"),
                        scheduled_service="yes",
                        icao="OMDB",
                        iata="DXB",
                        gps_code="OMDB",
                        name_russian=None,
                    ),
                    origin_airport=AirportFullInfoDTO(
                        id=78233,
                        name="Sheremetyevo International Airport",
                        continent="EU",
                        country=Country(id=183, iso="RU", name="Россия", name_english="Russia"),
                        region=Region(
                            id=111, iso="RU-MOS", name="Московская область", name_english="Moskovskaya oblast"
                        ),
                        city=City(id=2342, name="Москва", name_english="Moscow"),
                        scheduled_service="yes",
                        icao="UUEE",
                        iata="SVO",
                        gps_code="UUEE",
                        name_russian="Международный аэропорт Шереметьево",
                    ),
                    airline=Airline(
                        id=379, iata="N4", icao="NWS", name="Nordwind Airlines", name_russian="Nordwind Airlines"
                    ),
                    departure_at=datetime.datetime(2025, 8, 31, 18, 15, tzinfo=datetime.timezone.utc),
                    return_at=datetime.datetime(2025, 9, 7, 15, 50, tzinfo=datetime.timezone.utc),
                    duration=1165,
                    status="confirmed",
                    seat_class="economy",
                )
            ],
        ),
        TicketFullInfoDTO(
            id=212,
            duration=1995,
            price=43507.0,
            currency="RUB",
            transfers=2,
            segments=[
                TicketSegmentFullInfoDTO(
                    id=177,
                    flight_number="275",
                    destination_airport=AirportFullInfoDTO(
                        id=51072,
                        name="Dubai International Airport",
                        continent="AS",
                        country=Country(id=233, iso="AE", name="Объединенные Арабские Эмираты", name_english="UAE"),
                        region=None,
                        city=City(id=930, name="Дубай", name_english="Dubai"),
                        scheduled_service="yes",
                        icao="OMDB",
                        iata="DXB",
                        gps_code="OMDB",
                        name_russian=None,
                    ),
                    origin_airport=AirportFullInfoDTO(
                        id=78233,
                        name="Sheremetyevo International Airport",
                        continent="EU",
                        country=Country(id=183, iso="RU", name="Россия", name_english="Russia"),
                        region=Region(
                            id=111, iso="RU-MOS", name="Московская область", name_english="Moskovskaya oblast"
                        ),
                        city=City(id=2342, name="Москва", name_english="Moscow"),
                        scheduled_service="yes",
                        icao="UUEE",
                        iata="SVO",
                        gps_code="UUEE",
                        name_russian="Международный аэропорт Шереметьево",
                    ),
                    airline=Airline(id=737, iata="5N", icao="AUL", name="Smartavia", name_russian="Смартавиа"),
                    departure_at=datetime.datetime(2025, 8, 31, 14, 25, tzinfo=datetime.timezone.utc),
                    return_at=datetime.datetime(2025, 9, 3, 14, 5, tzinfo=datetime.timezone.utc),
                    duration=1995,
                    status="confirmed",
                    seat_class="economy",
                )
            ],
        ),
    ]
    assert result == expected_result
