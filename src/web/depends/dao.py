from src.infrastructure.persistence.dao.airport_dao import AirportDAO
from src.infrastructure.persistence.dao.tickets_dao import TicketDAO
from src.web.depends.annotations.db_annotation import DbAnnotation


def get_ticket_dao(db: DbAnnotation) -> TicketDAO:
    return TicketDAO(db)


def get_airport_dao(db: DbAnnotation) -> AirportDAO:
    return AirportDAO(db)
