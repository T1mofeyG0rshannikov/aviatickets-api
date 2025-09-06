from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from src.entities.tickets.ticket_entity.ticket import Ticket
from src.entities.tickets.tickets_repository import TicketRepositoryInterface
from src.entities.tickets.value_objects.unique_key import TicketUniqueKey
from src.entities.value_objects.entity_id import EntityId
from src.infrastructure.persistence.db.models.models import (
    TicketItineraryOrm,
    TicketOrm,
    TicketSegmentOrm,
)
from src.infrastructure.persistence.repositories.base_repository import BaseRepository
from src.infrastructure.persistence.repositories.mappers.ticket import orm_to_ticket


class TicketRepository(TicketRepositoryInterface, BaseRepository):
    async def get(self, id: EntityId) -> Ticket | None:
        result = await self.db.execute(
            select(TicketOrm)
            .options(joinedload(TicketOrm.itineraries).joinedload(TicketItineraryOrm.segments))
            .where(TicketOrm.id == id.value)
        )
        ticket = result.scalar()
        return orm_to_ticket(ticket) if ticket else None

    async def all_unique_keys(self) -> set[TicketUniqueKey]:
        results = await self.db.execute(select(TicketOrm.unique_key))
        keys = results.scalars().all()
        return {TicketUniqueKey(value=ticket) for ticket in keys}

    async def save_many(self, tickets: list[Ticket]) -> None:
        try:
            for ticket in tickets:
                ticket_orm = TicketOrm(
                    id=ticket.id.value,
                    price=ticket.price.value,
                    unique_key=str(ticket.unique_key.value),
                    currency=ticket.price.currency,
                )

                self.db.add(ticket_orm)
                await self.db.flush()

                itineraries_orm = [
                    TicketItineraryOrm(
                        id=itinerary.id.value,
                        duration=itinerary.duration,
                        ticket_id=ticket_orm.id,
                        transfers=itinerary.transfers,
                    )
                    for itinerary in ticket.itineraries
                ]

                self.db.add_all(itineraries_orm)
                await self.db.flush()

                segments_orm = [
                    TicketSegmentOrm(
                        id=segment.id.value,
                        segment_number=segment.segment_number,
                        origin_airport_id=segment.origin_airport_id.value,
                        destination_airport_id=segment.destination_airport_id.value,
                        airline_id=segment.airline_id.value,
                        departure_at=segment.departure_at.value,
                        return_at=segment.return_at.value,
                        duration=segment.duration,
                        flight_number=segment.flight_number.value,
                        ticket_itinerary_id=itinerary.id.value,
                        status=segment.status,
                        seat_class=segment.seat_class,
                    )
                    for itinerary in ticket.itineraries
                    for segment in itinerary.segments
                ]

                self.db.add_all(segments_orm)

            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise e
