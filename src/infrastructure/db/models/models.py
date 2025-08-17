from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.types import TIMESTAMP

from src.infrastructure.db.database import Model


class AirportOrm(Model):
    __tablename__ = "airports"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    continent = Column(String)

    country_id = Column(Integer, ForeignKey("countries.id"))
    country = relationship("CountryOrm", back_populates="airports")

    region_id = Column(Integer, ForeignKey("regions.id"))
    region = relationship("RegionOrm", back_populates="airports")

    city_id = Column(Integer, ForeignKey("cities.id"), index=True)
    city = relationship("CityOrm", back_populates="airports")

    scheduled_service = Column(String)
    icao = Column(String, index=True)
    iata = Column(String, index=True)
    gps_code = Column(String)
    local_code = Column(String)

    name_russian = Column(String)

    origin_tickets = relationship(
        "TicketOrm", back_populates="origin_airport", foreign_keys="[TicketOrm.origin_airport_id]"
    )
    destination_tickets = relationship(
        "TicketOrm", back_populates="destination_airport", foreign_keys="[TicketOrm.destination_airport_id]"
    )

    def __str__(self) -> str:
        return self.name


class TicketOrm(Model):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    origin_airport_id = Column(Integer, ForeignKey("airports.id"), index=True)
    origin_airport = relationship(AirportOrm, back_populates="origin_tickets", foreign_keys=[origin_airport_id])
    destination_airport_id = Column(Integer, ForeignKey("airports.id"), index=True)
    destination_airport = relationship(
        AirportOrm, back_populates="destination_tickets", foreign_keys=[destination_airport_id]
    )
    airline_id = Column(Integer, ForeignKey("airlines.id"), index=True)
    airline = relationship("AirlineOrm", back_populates="tickets")
    departure_at = Column(TIMESTAMP(timezone=True))
    return_at = Column(TIMESTAMP(timezone=True))
    duration = Column(Integer)
    price = Column(Integer)
    transfers = Column(Integer)

    user_tickets = relationship("UserTicketOrm", back_populates="ticket")


class UserOrm(Model):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
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

    id = Column(Integer, primary_key=True, index=True)
    icao = Column(String, nullable=True, index=True)
    iata = Column(String, nullable=True, index=True)
    name = Column(String)
    name_russian = Column(String)

    tickets = relationship(TicketOrm, back_populates="airline")

    def __str__(self) -> str:
        return self.name


class CountryOrm(Model):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    iso = Column(String, index=True)
    name = Column(String)
    name_english = Column(String)

    regions = relationship("RegionOrm", back_populates="country")

    airports = relationship(AirportOrm, back_populates="country")

    def __str__(self) -> str:
        return self.name


class RegionOrm(Model):
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)
    iso = Column(String, index=True)
    name = Column(String)
    name_english = Column(String)

    country_id = Column(Integer, ForeignKey("countries.id"), index=True)
    country = relationship(CountryOrm, back_populates="regions")

    airports = relationship(AirportOrm, back_populates="region")

    def __str__(self) -> str:
        return self.name


class CityOrm(Model):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    name_english = Column(String)

    airports = relationship(AirportOrm, back_populates="city")

    def __str__(self) -> str:
        return self.name


class UserTicketOrm(Model):
    __tablename__ = "usertickets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship(UserOrm, back_populates="tickets")

    ticket_id = Column(Integer, ForeignKey("tickets.id"))
    ticket = relationship(TicketOrm, back_populates="user_tickets")

    passengers = relationship("PassengerOrm", back_populates="user_ticket")


class PassengerOrm(Model):
    __tablename__ = "passangers"

    id = Column(Integer, primary_key=True, index=True)

    user_ticket_id = Column(Integer, ForeignKey("usertickets.id"))
    user_ticket = relationship(UserTicketOrm, back_populates="passengers")
    gender = Column(String)
    first_name = Column(String)
    second_name = Column(String)

    birth_date = Column(Date)

    def __str__(self) -> str:
        return f"{self.first_name} {self.second_name}"
