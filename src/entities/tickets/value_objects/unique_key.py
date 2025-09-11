from dataclasses import dataclass

from src.entities.tickets.ticket_entity.ticket import TicketItinerary


@dataclass(frozen=True)
class TicketUniqueKey:
    """
    Value Object for ticket unique key
    """

    value: int

    @classmethod
    def generate(cls, itineraries: list[TicketItinerary]):
        unique_string = ""

        for itinerary in itineraries:
            for segment in itinerary.segments:
                unique_string += f"{segment.flight_number};{segment.departure_at};{segment.return_at};{segment.origin_airport.id};{segment.destination_airport.id}"

        return cls(value=hash(unique_string))

    @classmethod
    def restore(cls, unique_key_value: int):
        return cls(value=unique_key_value)

    def __str__(self):
        return self.value
