from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from src.entities.tickets.dto import CreateAviaTicketDTO
from src.entities.tickets.ticket import Ticket
from src.infrastructure.db.mappers.ticket import orm_to_ticket
from src.infrastructure.db.models.models import TicketOrm, TicketSegmentOrm
from src.infrastructure.repositories.base_repository import BaseRepository


class TicketRepository(BaseRepository):
    async def get(self, id: int) -> Ticket:
        result = await self.db.execute(
            select(TicketOrm).join(TicketSegmentOrm).options(joinedload(TicketOrm.segments)).where(TicketOrm.id == id)
        )
        ticket = result.scalar()
        return orm_to_ticket(ticket) if ticket else None

    async def all(self) -> list[Ticket]:
        results = await self.db.execute(
            select(TicketOrm).join(TicketSegmentOrm).options(joinedload(TicketOrm.segments))
        )
        tickets = results.scalars().unique()
        return [orm_to_ticket(ticket) for ticket in tickets]

    async def create_many(self, tickets: list[CreateAviaTicketDTO]) -> None:
        try:
            for ticket in tickets:
                ticket_orm = TicketOrm(
                    duration=ticket.duration,
                    price=ticket.price,
                    currency=ticket.currency,
                    transfers=ticket.transfers,
                )

                self.db.add(ticket_orm)
                await self.db.flush()

                segments_orm = [
                    TicketSegmentOrm(
                        origin_airport_id=segment.origin_airport_id,
                        destination_airport_id=segment.destination_airport_id,
                        airline_id=segment.airline_id,
                        departure_at=segment.departure_at,
                        return_at=segment.return_at,
                        duration=segment.duration,
                        flight_number=segment.flight_number,
                        ticket_id=ticket_orm.id,
                        status=segment.status,
                        seat_class=segment.seat_class,
                    )
                    for segment in ticket.segments
                ]

                self.db.add_all(segments_orm)

            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e
