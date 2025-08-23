from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from src.entities.tickets.ticket import Ticket
from src.entities.tickets.tickets_repository import TicketRepositoryInterface
from src.entities.value_objects.entity_id import EntityId
from src.infrastructure.persistence.db.models.models import TicketOrm, TicketSegmentOrm
from src.infrastructure.persistence.repositories.base_repository import BaseRepository
from src.infrastructure.persistence.repositories.mappers.ticket import orm_to_ticket


class TicketRepository(TicketRepositoryInterface, BaseRepository):
    async def get(self, id: EntityId) -> Ticket:
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

    async def save_many(self, tickets: list[Ticket]) -> None:
        try:
            for ticket in tickets:
                ticket_orm = TicketOrm(
                    id=ticket.id.value,
                    duration=ticket.duration,
                    price=ticket.price,
                    currency=ticket.currency,
                    transfers=ticket.transfers,
                )

                self.db.add(ticket_orm)
                await self.db.flush()

                segments_orm = [
                    TicketSegmentOrm(
                        id=segment.id.value,
                        segment_number=segment.segment_number,
                        origin_airport_id=segment.origin_airport_id.value,
                        destination_airport_id=segment.destination_airport_id.value,
                        airline_id=segment.airline_id.value,
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
