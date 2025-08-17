import datetime

import pytest

from src.dto.airport import AirportFullInfoDTO
from src.entities.airline.airline import Airline
from src.entities.city import City
from src.entities.country.country import Country
from src.entities.region.region import Region
from src.entities.tickets.filters import TicketsFilter
from src.usecases.tickets.filter.dto import TicketFullInfoDTO
from src.usecases.tickets.filter.usecase import FilterTickets


@pytest.fixture
async def filter_tickets(ticket_read_repository) -> FilterTickets:
    return FilterTickets(ticket_read_repository)


@pytest.mark.asyncio
async def test_call_returns_filtered_tickets(filter_tickets: FilterTickets, populate_db):
    filters = TicketsFilter(
        price_min=30000,
        price_max=40000,
        airline_ids=[499],
        origin_airport_ids=[78233, 51072],
        destination_airport_ids=[51072, 78233],
        duration_min=500,
        duration_max=2000,
        transfers=1,
        departure_at=datetime.datetime(year=2024, month=9, day=18),
        return_at=datetime.datetime(year=2026, month=9, day=18),
    )
    result = await filter_tickets(filters)
    expected_result = [
        TicketFullInfoDTO(
            id=5,
            origin_airport=AirportFullInfoDTO(
                id=78233,
                name="Sheremetyevo International Airport",
                continent="EU",
                country=Country(id=183, iso="RU", name="Россия", name_english="Russian Federation"),
                region=Region(id=111, iso="RU-MOS", name="Московская область", name_english=None),
                city=City(id=2342, name="Москва", name_english="Moscow"),
                scheduled_service="yes",
                icao="UUEE",
                iata="SVO",
                gps_code="UUEE",
                name_russian="Международный аэропорт Шереметьево",
            ),
            destination_airport=AirportFullInfoDTO(
                id=51072,
                name="Dubai International Airport",
                continent="AS",
                country=Country(
                    id=233, iso="AE", name="Объединенные Арабские Эмираты", name_english="United Arab Emirates"
                ),
                region=None,
                city=City(id=930, name="Дубай", name_english="Dubai"),
                scheduled_service="yes",
                icao="OMDB",
                iata="DXB",
                gps_code="OMDB",
                name_russian="None",
            ),
            airline=Airline(id=616, iata="W5", icao="IRM", name="Mahan Airlines", name_russian="Махан Аирлинес"),
            departure_at=datetime.datetime(2025, 8, 19, 8, 10, tzinfo=datetime.timezone.utc),
            return_at=datetime.datetime(2025, 9, 6, 18, 10, tzinfo=datetime.timezone.utc),
            duration=1245,
            price=38825,
            transfers=1,
        ),
        TicketFullInfoDTO(
            id=14,
            origin_airport=AirportFullInfoDTO(
                id=78233,
                name="Sheremetyevo International Airport",
                continent="EU",
                country=Country(id=183, iso="RU", name="Россия", name_english="Russian Federation"),
                region=Region(id=111, iso="RU-MOS", name="Московская область", name_english=None),
                city=City(id=2342, name="Москва", name_english="Moscow"),
                scheduled_service="yes",
                icao="UUEE",
                iata="SVO",
                gps_code="UUEE",
                name_russian="Международный аэропорт Шереметьево",
            ),
            destination_airport=AirportFullInfoDTO(
                id=51072,
                name="Dubai International Airport",
                continent="AS",
                country=Country(
                    id=233, iso="AE", name="Объединенные Арабские Эмираты", name_english="United Arab Emirates"
                ),
                region=None,
                city=City(id=930, name="Дубай", name_english="Dubai"),
                scheduled_service="yes",
                icao="OMDB",
                iata="DXB",
                gps_code="OMDB",
                name_russian="None",
            ),
            airline=Airline(id=616, iata="W5", icao="IRM", name="Mahan Airlines", name_russian="Махан Аирлинес"),
            departure_at=datetime.datetime(2025, 8, 19, 8, 10, tzinfo=datetime.timezone.utc),
            return_at=datetime.datetime(2025, 9, 15, 18, 10, tzinfo=datetime.timezone.utc),
            duration=1245,
            price=37212,
            transfers=1,
        ),
    ]
    print(result, "result")

    assert result == expected_result
