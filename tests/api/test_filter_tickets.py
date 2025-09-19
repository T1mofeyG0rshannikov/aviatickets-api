import api.mock_tickets as mock_tickets
from fastapi.testclient import TestClient


def test_filter_tickets(client: TestClient, populate_db):
    response = client.post(
        "/filter-tickets",
        json={
            "price_min": 0,
            "price_max": 86037,
            "airline_ids": ["bc444200-eab9-4d76-a6bf-55fdd93a4965"],
            "origin_airport_ids": ["bda7b0bf-1163-4f88-a089-73672b892d9d"],
            "destination_airport_ids": ["20a22957-7d96-4b70-ad81-f35d8f76770b"],
        },
    )

    assert response.status_code == 200
    print(response.json())

    expected_data = mock_tickets.ALL_TICKETS_MOCK

    data = response.json()
    assert data == expected_data
