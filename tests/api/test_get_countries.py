import api.mocks as mocks
from fastapi.testclient import TestClient


def test_get_countries(client: TestClient, populate_db):
    start_with = "Р"
    response = client.get(f"/countries/{start_with}")

    assert response.status_code == 200
    print(response.json())

    expected_data = mocks.MOCK_COUNTRIES

    data = response.json()
    for country in data:
        country["airports"] = set(country["airports"])

    for country in expected_data:
        country["airports"] = set(country["airports"])

    assert data == expected_data
