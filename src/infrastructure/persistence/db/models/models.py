import uuid

from sqlalchemy import UUID, Boolean, Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import TIMESTAMP

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

    ticket_id = Column(UUID(as_uuid=True), ForeignKey("tickets.id"))
    ticket = relationship("TicketOrm", back_populates="segments")


class TicketOrm(Model):
    __tablename__ = "tickets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    duration = Column(Integer)
    price = Column(Float, index=True)
    currency = Column(String)
    transfers = Column(Integer)

    user_tickets = relationship("UserTicketOrm", back_populates="ticket")
    segments = relationship("TicketSegmentOrm", back_populates="ticket")


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


class PassengerOrm(Model):
    __tablename__ = "passangers"

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
