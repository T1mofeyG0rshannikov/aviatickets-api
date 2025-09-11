import uuid

from sqlalchemy import UUID, Boolean, Column, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import DetachedInstanceError
from sqlalchemy.types import TIMESTAMP

from src.entities.airport.airport import Airport
from src.infrastructure.persistence.db.database import Model


class AirportOrm(Model):
    __tablename__ = "airports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String)
    continent = Column(String)

    country_id = Column(UUID(as_uuid=True), ForeignKey("countries.id"))
    country = relationship("CountryOrm", back_populates="airports")

    region_id = Column(UUID(as_uuid=True), ForeignKey("regions.id"))
    region = relationship("RegionOrm", back_populates="airports")

    city_id = Column(UUID(as_uuid=True), ForeignKey("cities.id"), index=True)
    city = relationship("CityOrm", back_populates="airports")

    scheduled_service = Column(String)
    icao = Column(String, index=True)
    iata = Column(String, index=True)
    gps_code = Column(String)
    local_code = Column(String)

    name_russian = Column(String)

    origin_tickets = relationship(
        "TicketSegmentOrm", back_populates="origin_airport", foreign_keys="[TicketSegmentOrm.origin_airport_id]"
    )
    destination_tickets = relationship(
        "TicketSegmentOrm",
        back_populates="destination_airport",
        foreign_keys="[TicketSegmentOrm.destination_airport_id]",
    )

    def __str__(self) -> str:
        return self.name

    @classmethod
    def from_entity(cls, airport: Airport) -> "AirportOrm":
        return AirportOrm(
            id=airport.id.value,
            name=airport.name.value,
            continent=airport.continent,
            country_id=airport.country_id.value if airport.country_id else None,
            region_id=airport.region_id.value if airport.region_id else None,
            city_id=airport.city_id.value if airport.city_id else None,
            scheduled_service=airport.scheduled_service,
            icao=airport.icao,
            iata=airport.iata,
            gps_code=airport.gps_code,
            local_code=airport.local_code,
            name_russian=airport.name_russian.value if airport.name_russian else None,
        )


class TicketSegmentOrm(Model):
    __tablename__ = "ticketsegments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    origin_airport_id = Column(UUID(as_uuid=True), ForeignKey("airports.id"), index=True)
    origin_airport = relationship(AirportOrm, back_populates="origin_tickets", foreign_keys=[origin_airport_id])
    destination_airport_id = Column(UUID(as_uuid=True), ForeignKey("airports.id"), index=True)
    destination_airport = relationship(
        AirportOrm, back_populates="destination_tickets", foreign_keys=[destination_airport_id]
    )
    airline_id = Column(UUID(as_uuid=True), ForeignKey("airlines.id"), index=True)
    airline = relationship("AirlineOrm", back_populates="tickets")
    departure_at = Column(TIMESTAMP(timezone=True))
    return_at = Column(TIMESTAMP(timezone=True))
    duration = Column(Integer)
    flight_number = Column(String)
    segment_number = Column(Integer)
    status = Column(String)
    seat_class = Column(String)

    ticket_itinerary_id = Column(UUID(as_uuid=True), ForeignKey("ticketitineraries.id"))
    ticket_itinerary = relationship("TicketItineraryOrm", back_populates="segments")

    def __str__(self) -> str:
        try:
            return f"{self.flight_number}: {self.origin_airport.iata} -> {self.destination_airport.iata} ({self.departure_at.strftime('%Y-%m-%d %H:%M')})"
        except DetachedInstanceError:
            return super().__str__()


class TicketItineraryOrm(Model):
    __tablename__ = "ticketitineraries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    duration = Column(Integer)

    ticket_id = Column(UUID(as_uuid=True), ForeignKey("tickets.id"))
    ticket = relationship("TicketOrm", back_populates="itineraries")

    transfers = Column(Integer)

    segments = relationship("TicketSegmentOrm", back_populates="ticket_itinerary")

    def __str__(self) -> str:
        try:
            return f"""Itinerary: {", ".join([str(s) for s in self.segments])}"""
        except DetachedInstanceError:
            return super().__str__()


class TicketOrm(Model):
    __tablename__ = "tickets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    unique_key = Column(String, nullable=True, unique=True)
    price = Column(Numeric(10, 2), index=True)
    currency = Column(String)

    user_tickets = relationship("UserTicketOrm", back_populates="ticket")
    itineraries = relationship("TicketItineraryOrm", back_populates="ticket")


class UserOrm(Model):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(String)
    second_name = Column(String)
    email = Column(String, unique=True)
    hash_password = Column(String)
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

    tickets = relationship("UserTicketOrm", back_populates="user")
    insurances = relationship("InsuranceOrm", back_populates="insured")

    def __str__(self) -> str:
        return self.email


class AirlineOrm(Model):
    __tablename__ = "airlines"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    icao = Column(String, nullable=True, index=True)
    iata = Column(String, nullable=True, index=True)
    name = Column(String)
    name_russian = Column(String)

    tickets = relationship(TicketSegmentOrm, back_populates="airline")

    def __str__(self) -> str:
        return self.name


class CountryOrm(Model):
    __tablename__ = "countries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    iso = Column(String, index=True)
    name = Column(String)
    name_english = Column(String)

    regions = relationship("RegionOrm", back_populates="country")

    airports = relationship(AirportOrm, back_populates="country")

    def __str__(self) -> str:
        return self.name


class RegionOrm(Model):
    __tablename__ = "regions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    iso = Column(String, index=True)
    name = Column(String)
    name_english = Column(String)

    country_id = Column(UUID(as_uuid=True), ForeignKey("countries.id"), index=True)
    country = relationship(CountryOrm, back_populates="regions")

    airports = relationship(AirportOrm, back_populates="region")

    def __str__(self) -> str:
        return self.name


class CityOrm(Model):
    __tablename__ = "cities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    name_english = Column(String)

    airports = relationship(AirportOrm, back_populates="city")

    def __str__(self) -> str:
        return self.name


class UserTicketOrm(Model):
    __tablename__ = "usertickets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    user = relationship(UserOrm, back_populates="tickets")

    ticket_id = Column(UUID(as_uuid=True), ForeignKey("tickets.id"))
    ticket = relationship(TicketOrm, back_populates="user_tickets")

    passengers = relationship("PassengerOrm", back_populates="user_ticket")
    pdf = relationship("PdfTicketOrm", back_populates="user_ticket")


class PassengerOrm(Model):
    __tablename__ = "passengers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_ticket_id = Column(UUID(as_uuid=True), ForeignKey("usertickets.id"))
    user_ticket = relationship(UserTicketOrm, back_populates="passengers")
    gender = Column(String)
    first_name = Column(String)
    second_name = Column(String)

    birth_date = Column(Date)
    passport = Column(String)
    expiration_date = Column(Date)

    def __str__(self) -> str:
        return f"{self.first_name} {self.second_name}"


class PdfTicketOrm(Model):
    __tablename__ = "pdftickets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    user_ticket_id = Column(UUID(as_uuid=True), ForeignKey("usertickets.id"))
    user_ticket = relationship(UserTicketOrm, back_populates="pdf")

    name = Column(String)
    content_path = Column(String)


class InsuranceOrm(Model):
    __tablename__ = "insurances"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    contract = Column(String, unique=True)
    insured_id = Column(UUID(as_uuid=True), ForeignKey("user.id"))
    insured = relationship(UserOrm, back_populates="insurances")

    premium_value = Column(Numeric(10, 2))
    premium_currency = Column(String)

    created_at = Column(Date)
    start_date = Column(Date)
    end_date = Column(Date)

    territory = Column(String)

    pdf = relationship("PdfInsuranceOrm", back_populates="insurance")


class PdfInsuranceOrm(Model):
    __tablename__ = "pdfinsurances"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    insurance_id = Column(UUID(as_uuid=True), ForeignKey("insurances.id"))
    insurance = relationship(InsuranceOrm, back_populates="pdf")

    name = Column(String)
    content_path = Column(String)
