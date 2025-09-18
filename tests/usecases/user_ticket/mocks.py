import datetime
from decimal import Decimal
from uuid import UUID

from src.application.dto.aircraft import AircraftDTO
from src.application.dto.airline import AirlineDTO
from src.application.dto.airports.full_info import AirportFullInfoDTO
from src.application.dto.location import CityDTO, CountryDTO, RegionDTO
from src.application.dto.ticket import (
    TicketFullInfoDTO,
    TicketItineraryFullInfoDTO,
    TicketSegmentFullInfoDTO,
)
from src.application.dto.user import UserDTO
from src.application.dto.user_ticket import PassengerDTO, UserTicketFullInfoDTO
from src.entities.user.user import User
from src.entities.user.value_objects.birth_date import BirthDate
from src.entities.user.value_objects.email import Email
from src.entities.user.value_objects.first_name import FirstName
from src.entities.user.value_objects.second_name import SecondName
from src.entities.user.value_objects.user_id import UserId
from src.entities.value_objects.price.currency_enum import CurrencyEnum

MOCK_USER_TICKET_DTO = UserTicketFullInfoDTO(
    id=UUID("9f8619ce-2b4e-4a6d-b714-c523430bd5df"),
    user=UserDTO(
        id=UUID("0c95ad77-07b3-4516-accc-c96647dbbbb8"),
        first_name="Тимофей",
        second_name="Марков",
        email="tgorshannikov@mail.ru",
        birth_date=datetime.date(11, 11, 2000),
    ),
    ticket=TicketFullInfoDTO(
        id=UUID("fc1bab96-5edb-47cd-98df-08b3ae42e461"),
        price=Decimal("920.38"),
        currency=CurrencyEnum.eur,
        itineraries=[
            TicketItineraryFullInfoDTO(
                id=UUID("9e1ba5dd-a3c8-4bcc-9392-35e75517e808"),
                transfers=1,
                segments=[
                    TicketSegmentFullInfoDTO(
                        id=UUID("56ecd9f8-a44c-44d3-b127-2579d94d4254"),
                        flight_number="QR-338",
                        segment_number=1,
                        destination_airport=AirportFullInfoDTO(
                            id=UUID("21131c03-e842-4e20-b82d-20f3e650a0ce"),
                            name="Hamad International Airport",
                            continent="AS",
                            country=CountryDTO(
                                id=UUID("5cf32bc5-ab20-4e1c-a67e-0e88e6d890b7"),
                                iso="QA",
                                name="Катар",
                                name_english="Qatar",
                            ),
                            city=CityDTO(
                                id=UUID("785ae0dd-88fa-4574-a26c-f309d3e6a577"), name="Доха", name_english="Doha"
                            ),
                            scheduled_service="yes",
                            icao="OTHH",
                            iata="DOH",
                            gps_code="OTHH",
                            region=RegionDTO(
                                id=UUID("2821ead3-66d8-46b6-b564-4960fc78e956"),
                                iso="QA-DA",
                                name="Эд-Доха",
                                name_english="Doha",
                            ),
                            name_russian="Международный аэропорт Доха",
                        ),
                        origin_airport=AirportFullInfoDTO(
                            id=UUID("bda7b0bf-1163-4f88-a089-73672b892d9d"),
                            name="Sheremetyevo International Airport",
                            continent="EU",
                            country=CountryDTO(
                                id=UUID("9189b385-44db-4f74-b766-b60f213737c5"),
                                iso="RU",
                                name="Россия",
                                name_english="Russia",
                            ),
                            city=CityDTO(
                                id=UUID("68ef468b-9d14-4bb7-97ae-5c503d6abe0d"), name="Москва", name_english="Moscow"
                            ),
                            scheduled_service="yes",
                            icao="UUEE",
                            iata="SVO",
                            gps_code="UUEE",
                            region=RegionDTO(
                                id=UUID("3c236e36-ec1a-4106-9695-4a293d15a12a"),
                                iso="RU-MOS",
                                name="Московская область",
                                name_english="Moskovskaya oblast",
                            ),
                            name_russian="Международный аэропорт Шереметьево",
                        ),
                        airline=AirlineDTO(
                            id=UUID("bc444200-eab9-4d76-a6bf-55fdd93a4965"),
                            iata="QR",
                            icao="QTR",
                            name="Qatar Airways",
                            name_russian="Катарские Авиалинии",
                        ),
                        aircraft=AircraftDTO(name="Boeing 787-9 pax", iata="789"),
                        departure_at=datetime.datetime(2025, 9, 19, 20, 50, tzinfo=datetime.timezone.utc),
                        return_at=datetime.datetime(2025, 9, 20, 2, 15, tzinfo=datetime.timezone.utc),
                        duration=325,
                        status="confirmed",
                        seat_class="economy",
                    ),
                    TicketSegmentFullInfoDTO(
                        id=UUID("0b2721a0-8f02-4e18-9152-fa4f02d5496d"),
                        flight_number="QR-1022",
                        segment_number=2,
                        destination_airport=AirportFullInfoDTO(
                            id=UUID("20a22957-7d96-4b70-ad81-f35d8f76770b"),
                            name="Dubai International Airport",
                            continent="AS",
                            country=CountryDTO(
                                id=UUID("c2a801cb-1ec0-421b-ba4b-975dabc8567e"),
                                iso="AE",
                                name="Объединенные Арабские Эмираты",
                                name_english="United Arab Emirates",
                            ),
                            city=CityDTO(
                                id=UUID("98bcade0-7839-43a4-90ea-58bf1ca6d954"), name="Дубай", name_english="Dubai"
                            ),
                            scheduled_service="yes",
                            icao="OMDB",
                            iata="DXB",
                            gps_code="OMDB",
                            region=RegionDTO(
                                id=UUID("ba845903-1625-46f6-b74e-ae331dd01b9f"),
                                iso="AE-DU",
                                name="Дубай",
                                name_english="Dubai",
                            ),
                            name_russian=None,
                        ),
                        origin_airport=AirportFullInfoDTO(
                            id=UUID("21131c03-e842-4e20-b82d-20f3e650a0ce"),
                            name="Hamad International Airport",
                            continent="AS",
                            country=CountryDTO(
                                id=UUID("5cf32bc5-ab20-4e1c-a67e-0e88e6d890b7"),
                                iso="QA",
                                name="Катар",
                                name_english="Qatar",
                            ),
                            city=CityDTO(
                                id=UUID("785ae0dd-88fa-4574-a26c-f309d3e6a577"), name="Доха", name_english="Doha"
                            ),
                            scheduled_service="yes",
                            icao="OTHH",
                            iata="DOH",
                            gps_code="OTHH",
                            region=RegionDTO(
                                id=UUID("2821ead3-66d8-46b6-b564-4960fc78e956"),
                                iso="QA-DA",
                                name="Эд-Доха",
                                name_english="Doha",
                            ),
                            name_russian="Международный аэропорт Доха",
                        ),
                        airline=AirlineDTO(
                            id=UUID("bc444200-eab9-4d76-a6bf-55fdd93a4965"),
                            iata="QR",
                            icao="QTR",
                            name="Qatar Airways",
                            name_russian="Катарские Авиалинии",
                        ),
                        aircraft=AircraftDTO(name="Airbus A350-900", iata="359"),
                        departure_at=datetime.datetime(2025, 9, 20, 6, 20, tzinfo=datetime.timezone.utc),
                        return_at=datetime.datetime(2025, 9, 20, 7, 40, tzinfo=datetime.timezone.utc),
                        duration=80,
                        status="confirmed",
                        seat_class="economy",
                    ),
                ],
                duration=650,
            ),
            TicketItineraryFullInfoDTO(
                id=UUID("1526896a-8bfe-439c-afee-925999daf67a"),
                transfers=1,
                segments=[
                    TicketSegmentFullInfoDTO(
                        id=UUID("5b5eac2d-2239-4a9c-8876-be0d1ab36b9c"),
                        flight_number="QR-1007",
                        segment_number=1,
                        destination_airport=AirportFullInfoDTO(
                            id=UUID("21131c03-e842-4e20-b82d-20f3e650a0ce"),
                            name="Hamad International Airport",
                            continent="AS",
                            country=CountryDTO(
                                id=UUID("5cf32bc5-ab20-4e1c-a67e-0e88e6d890b7"),
                                iso="QA",
                                name="Катар",
                                name_english="Qatar",
                            ),
                            city=CityDTO(
                                id=UUID("785ae0dd-88fa-4574-a26c-f309d3e6a577"), name="Доха", name_english="Doha"
                            ),
                            scheduled_service="yes",
                            icao="OTHH",
                            iata="DOH",
                            gps_code="OTHH",
                            region=RegionDTO(
                                id=UUID("2821ead3-66d8-46b6-b564-4960fc78e956"),
                                iso="QA-DA",
                                name="Эд-Доха",
                                name_english="Doha",
                            ),
                            name_russian="Международный аэропорт Доха",
                        ),
                        origin_airport=AirportFullInfoDTO(
                            id=UUID("20a22957-7d96-4b70-ad81-f35d8f76770b"),
                            name="Dubai International Airport",
                            continent="AS",
                            country=CountryDTO(
                                id=UUID("c2a801cb-1ec0-421b-ba4b-975dabc8567e"),
                                iso="AE",
                                name="Объединенные Арабские Эмираты",
                                name_english="United Arab Emirates",
                            ),
                            city=CityDTO(
                                id=UUID("98bcade0-7839-43a4-90ea-58bf1ca6d954"), name="Дубай", name_english="Dubai"
                            ),
                            scheduled_service="yes",
                            icao="OMDB",
                            iata="DXB",
                            gps_code="OMDB",
                            region=RegionDTO(
                                id=UUID("ba845903-1625-46f6-b74e-ae331dd01b9f"),
                                iso="AE-DU",
                                name="Дубай",
                                name_english="Dubai",
                            ),
                            name_russian=None,
                        ),
                        airline=AirlineDTO(
                            id=UUID("bc444200-eab9-4d76-a6bf-55fdd93a4965"),
                            iata="QR",
                            icao="QTR",
                            name="Qatar Airways",
                            name_russian="Катарские Авиалинии",
                        ),
                        aircraft=AircraftDTO(name="Airbus A330-300", iata="333"),
                        departure_at=datetime.datetime(2025, 9, 27, 7, 45, tzinfo=datetime.timezone.utc),
                        return_at=datetime.datetime(2025, 9, 27, 9, 0, tzinfo=datetime.timezone.utc),
                        duration=75,
                        status="confirmed",
                        seat_class="economy",
                    ),
                    TicketSegmentFullInfoDTO(
                        id=UUID("9be4e665-91ad-4a74-9f42-3f700c8c569b"),
                        flight_number="QR-337",
                        segment_number=2,
                        destination_airport=AirportFullInfoDTO(
                            id=UUID("bda7b0bf-1163-4f88-a089-73672b892d9d"),
                            name="Sheremetyevo International Airport",
                            continent="EU",
                            country=CountryDTO(
                                id=UUID("9189b385-44db-4f74-b766-b60f213737c5"),
                                iso="RU",
                                name="Россия",
                                name_english="Russia",
                            ),
                            city=CityDTO(
                                id=UUID("68ef468b-9d14-4bb7-97ae-5c503d6abe0d"), name="Москва", name_english="Moscow"
                            ),
                            scheduled_service="yes",
                            icao="UUEE",
                            iata="SVO",
                            gps_code="UUEE",
                            region=RegionDTO(
                                id=UUID("3c236e36-ec1a-4106-9695-4a293d15a12a"),
                                iso="RU-MOS",
                                name="Московская область",
                                name_english="Moskovskaya oblast",
                            ),
                            name_russian="Международный аэропорт Шереметьево",
                        ),
                        origin_airport=AirportFullInfoDTO(
                            id=UUID("21131c03-e842-4e20-b82d-20f3e650a0ce"),
                            name="Hamad International Airport",
                            continent="AS",
                            country=CountryDTO(
                                id=UUID("5cf32bc5-ab20-4e1c-a67e-0e88e6d890b7"),
                                iso="QA",
                                name="Катар",
                                name_english="Qatar",
                            ),
                            city=CityDTO(
                                id=UUID("785ae0dd-88fa-4574-a26c-f309d3e6a577"), name="Доха", name_english="Doha"
                            ),
                            scheduled_service="yes",
                            icao="OTHH",
                            iata="DOH",
                            gps_code="OTHH",
                            region=RegionDTO(
                                id=UUID("2821ead3-66d8-46b6-b564-4960fc78e956"),
                                iso="QA-DA",
                                name="Эд-Доха",
                                name_english="Doha",
                            ),
                            name_russian="Международный аэропорт Доха",
                        ),
                        airline=AirlineDTO(
                            id=UUID("bc444200-eab9-4d76-a6bf-55fdd93a4965"),
                            iata="QR",
                            icao="QTR",
                            name="Qatar Airways",
                            name_russian="Катарские Авиалинии",
                        ),
                        aircraft=AircraftDTO(name="Boeing 787-9 pax", iata="789"),
                        departure_at=datetime.datetime(2025, 9, 27, 12, 50, tzinfo=datetime.timezone.utc),
                        return_at=datetime.datetime(2025, 9, 27, 18, 20, tzinfo=datetime.timezone.utc),
                        duration=330,
                        status="confirmed",
                        seat_class="economy",
                    ),
                ],
                duration=635,
            ),
        ],
    ),
    passengers=[
        PassengerDTO(
            id=UUID("32911dd0-7aff-45c5-b6a1-de1b3750fabe"), gender="string", first_name="string", second_name="string"
        )
    ],
)


MOCK_USER = User(
    id=UserId(value=UUID("0c95ad77-07b3-4516-accc-c96647dbbbb8")),
    first_name=FirstName("Тимофей"),
    second_name=SecondName("Марков"),
    email=Email("tgorshannikov@mail.ru"),
    hash_password="$2b$12$nfKvEXfUHAgKZRVPLwwD9.4edFLxtpyTF6SoEvqh2i0Ad4AeyiDQW",
    birth_date=BirthDate(value=datetime.date(2000, 1, 1)),
    is_superuser=True,
    is_active=True,
)
