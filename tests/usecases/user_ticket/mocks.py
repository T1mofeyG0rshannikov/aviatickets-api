import datetime
from decimal import Decimal
from uuid import UUID

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
from src.entities.value_objects.price.currency_enum import CurrencyEnum

mock_user_ticket_dto = UserTicketFullInfoDTO(
    id=UUID("946791d0-e73f-44cf-b7cf-93d2da8f3cc0"),
    user=UserDTO(
        id=UUID("0c95ad77-07b3-4516-accc-c96647dbbbb8"),
        first_name="Тимофей",
        second_name="Марков",
        email="tgorshannikov@mail.ru",
    ),
    ticket=TicketFullInfoDTO(
        id=UUID("ea0a55d3-ce52-4596-b026-ac482d7a3403"),
        price=Decimal("961.62"),
        currency=CurrencyEnum.eur,
        itineraries=[
            TicketItineraryFullInfoDTO(
                id=UUID("d0d5a429-29b6-4f1e-9184-46f9dd0829e1"),
                transfers=1,
                segments=[
                    TicketSegmentFullInfoDTO(
                        id=UUID("36759260-9aa9-4d61-8f64-a7b4a4638aac"),
                        flight_number="QR-340",
                        segment_number=1,
                        destination_airport=AirportFullInfoDTO(
                            id=UUID("1d69dae8-8304-4627-b9cd-4c1510df9a90"),
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
                            region=None,
                            name_russian=None,
                        ),
                        origin_airport=AirportFullInfoDTO(
                            id=UUID("22ec4f30-a186-47b6-9b20-c753fd29ce5d"),
                            name="Sheremetyevo International Airport",
                            continent="EU",
                            country=CountryDTO(
                                id=UUID("9189b385-44db-4f74-b766-b60f213737c5"),
                                iso="RU",
                                name="Россия",
                                name_english="Russia",
                            ),
                            city=CityDTO(
                                id=UUID("68ef468b-9d14-4bb7-97ae-5c503d6abe0d"),
                                name="Москва",
                                name_english="Moscow",
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
                        departure_at=datetime.datetime(2025, 9, 4, 14, 5, tzinfo=datetime.timezone.utc),
                        return_at=datetime.datetime(2025, 9, 4, 19, 30, tzinfo=datetime.timezone.utc),
                        duration=325,
                        status="confirmed",
                        seat_class="premium economy",
                    ),
                    TicketSegmentFullInfoDTO(
                        id=UUID("5f66ce96-dc81-437a-b5ff-86a1fdba8398"),
                        flight_number="QR-1002",
                        segment_number=2,
                        destination_airport=AirportFullInfoDTO(
                            id=UUID("283aed83-e7b2-4b90-b892-00e7eb814d21"),
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
                            region=None,
                            name_russian=None,
                        ),
                        origin_airport=AirportFullInfoDTO(
                            id=UUID("1d69dae8-8304-4627-b9cd-4c1510df9a90"),
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
                            region=None,
                            name_russian=None,
                        ),
                        airline=AirlineDTO(
                            id=UUID("bc444200-eab9-4d76-a6bf-55fdd93a4965"),
                            iata="QR",
                            icao="QTR",
                            name="Qatar Airways",
                            name_russian="Катарские Авиалинии",
                        ),
                        departure_at=datetime.datetime(2025, 9, 4, 22, 15, tzinfo=datetime.timezone.utc),
                        return_at=datetime.datetime(2025, 9, 4, 23, 35, tzinfo=datetime.timezone.utc),
                        duration=80,
                        status="confirmed",
                        seat_class="premium economy",
                    ),
                ],
                duration=570,
            ),
            TicketItineraryFullInfoDTO(
                id=UUID("592ae00b-4119-4c5c-acfe-16801d566603"),
                transfers=1,
                segments=[
                    TicketSegmentFullInfoDTO(
                        id=UUID("2e495614-33ff-4744-a1ee-ad5f9e9da80e"),
                        flight_number="QR-1023",
                        segment_number=1,
                        destination_airport=AirportFullInfoDTO(
                            id=UUID("1d69dae8-8304-4627-b9cd-4c1510df9a90"),
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
                            region=None,
                            name_russian=None,
                        ),
                        origin_airport=AirportFullInfoDTO(
                            id=UUID("283aed83-e7b2-4b90-b892-00e7eb814d21"),
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
                            region=None,
                            name_russian=None,
                        ),
                        airline=AirlineDTO(
                            id=UUID("bc444200-eab9-4d76-a6bf-55fdd93a4965"),
                            iata="QR",
                            icao="QTR",
                            name="Qatar Airways",
                            name_russian="Катарские Авиалинии",
                        ),
                        departure_at=datetime.datetime(2025, 9, 10, 9, 15, tzinfo=datetime.timezone.utc),
                        return_at=datetime.datetime(2025, 9, 10, 10, 30, tzinfo=datetime.timezone.utc),
                        duration=75,
                        status="confirmed",
                        seat_class="premium economy",
                    ),
                    TicketSegmentFullInfoDTO(
                        id=UUID("43ce36e7-f90c-43e4-a012-d301b0c24f1b"),
                        flight_number="QR-337",
                        segment_number=2,
                        destination_airport=AirportFullInfoDTO(
                            id=UUID("22ec4f30-a186-47b6-9b20-c753fd29ce5d"),
                            name="Sheremetyevo International Airport",
                            continent="EU",
                            country=CountryDTO(
                                id=UUID("9189b385-44db-4f74-b766-b60f213737c5"),
                                iso="RU",
                                name="Россия",
                                name_english="Russia",
                            ),
                            city=CityDTO(
                                id=UUID("68ef468b-9d14-4bb7-97ae-5c503d6abe0d"),
                                name="Москва",
                                name_english="Moscow",
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
                            id=UUID("1d69dae8-8304-4627-b9cd-4c1510df9a90"),
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
                            region=None,
                            name_russian=None,
                        ),
                        airline=AirlineDTO(
                            id=UUID("bc444200-eab9-4d76-a6bf-55fdd93a4965"),
                            iata="QR",
                            icao="QTR",
                            name="Qatar Airways",
                            name_russian="Катарские Авиалинии",
                        ),
                        departure_at=datetime.datetime(2025, 9, 10, 12, 50, tzinfo=datetime.timezone.utc),
                        return_at=datetime.datetime(2025, 9, 10, 18, 20, tzinfo=datetime.timezone.utc),
                        duration=330,
                        status="confirmed",
                        seat_class="premium economy",
                    ),
                ],
                duration=545,
            ),
        ],
    ),
    passengers=[
        PassengerDTO(
            id=UUID("664014a4-fdf9-4176-9f10-6fdb3eedf3dd"),
            gender="string",
            first_name="string",
            second_name="string",
        )
    ],
)
