from dataclasses import dataclass

from avia.entities.airport.airport import Airport
from avia.entities.tickets.exceptions import EmptyTicketSegmentsError
from avia.entities.tickets.ticket_entity.ticket_segment import TicketSegment
from avia.entities.value_objects.entity_id import EntityId


@dataclass
class TicketItinerary:
    id: EntityId
    transfers: int
    segments: list[TicketSegment]
    duration: int

    @property
    def origin_airport(self) -> Airport:
        return self.segments[0].origin_airport

    @property
    def destination_airport(self) -> Airport:
        return self.segments[-1].destination_airport

    @classmethod
    def create(cls, segments: list[TicketSegment], duration: int):
        if len(segments) == 0:
            raise EmptyTicketSegmentsError

        return cls(id=EntityId.generate(), transfers=len(segments) - 1, segments=segments, duration=duration)
