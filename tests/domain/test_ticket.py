from src.entities.tickets.value_objects.unique_key import TicketUniqueKey


def test_unique_keys_list_contains():
    keys = [
        TicketUniqueKey(value=123),
        TicketUniqueKey(value=234),
        TicketUniqueKey(value=345),
    ]

    assert TicketUniqueKey(value=123) in keys
