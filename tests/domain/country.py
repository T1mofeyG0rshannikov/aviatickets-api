import uuid

import pytest

from src.entities.location.country.country import Country
from src.entities.value_objects.entity_id import EntityId


@pytest.mark
def test_create_region():
    region = Country.create(
        iso="RU",
        name="Россия",
        name_english="Russia",
    )

    assert isinstance(region, Country)


@pytest.mark
def test_create_region_with_invalid_iso():
    invalid_iso = "R1U-M3OS"
    with pytest.raises(ValueError) as excinfo:
        Country.create(
            iso=invalid_iso,
            name="Россия",
            name_english="Russia",
        )

    assert f"'{invalid_iso}' is not a valid ISO code." in str(excinfo.value)
