from dataclasses import dataclass

from src.entities.tickets.exceptions import EmptyTicketSegmentsError
from src.entities.tickets.ticket_entity.ticket_segment import TicketSegment
from src.entities.value_objects.entity_id import EntityId


@dataclass
class TicketItinerary:
    id: EntityId
    transfers: int
    segments: list[TicketSegment]
    duration: int

    @classmethod
    def create(cls, segments: list[TicketSegment], duration: int):
        if len(segments) == 0:
            raise EmptyTicketSegmentsError

        return cls(id=EntityId.generate(), transfers=len(segments) - 1, segments=segments, duration=duration)
