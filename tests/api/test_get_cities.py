import api.mocks as mocks
from fastapi.testclient import TestClient


def test_get_cities(client: TestClient, populate_db):
    start_with = "М"
    response = client.get(f"/cities/{start_with}")

    assert response.status_code == 200
    print(response.json())

    expected_data = mocks.MOCK_CITIES

    data = response.json()
    for city in data:
        city["airports"] = set(city["airports"])

    for city in expected_data:
        city["airports"] = set(city["airports"])

    assert data == expected_data
