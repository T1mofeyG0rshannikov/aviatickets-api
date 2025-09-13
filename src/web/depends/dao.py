from src.infrastructure.persistence.dao.airport_dao import AirportDAO
from src.infrastructure.persistence.dao.cities_dao import CitiestDAO
from src.infrastructure.persistence.dao.countries_dao import CountriesDAO
from src.infrastructure.persistence.dao.tickets_dao import TicketDAO
from src.web.depends.annotations.db_annotation import DbAnnotation


def get_ticket_dao(db: DbAnnotation) -> TicketDAO:
    return TicketDAO(db)


def get_airport_dao(db: DbAnnotation) -> AirportDAO:
    return AirportDAO(db)


def get_cities_dao(db: DbAnnotation) -> CitiestDAO:
    return CitiestDAO(db)


def get_countries_dao(db: DbAnnotation) -> CountriesDAO:
    return CountriesDAO(db)
