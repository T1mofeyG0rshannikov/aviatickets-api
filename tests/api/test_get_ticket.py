import api.mock_tickets as mock_tickets
import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_get_tickets(client: TestClient, populate_db):
    ticket_id = "a96d3a5b-edc3-44dc-8984-3fd307a46a60"
    response = client.get(f"/ticket/{ticket_id}")
    print(response)
    # assert response.status_code == 200

    expected_data = mock_tickets.MOCK_TICKET

    data = response.json()
    print(data)
    assert data == expected_data
