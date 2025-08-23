import uuid

import pytest

from src.entities.location.region.region import Region
from src.entities.value_objects.entity_id import EntityId


@pytest.mark
def test_create_region():
    region = Region.create(iso="RU-MOS", name="Москва", name_english="Moscow", country_id=EntityId(uuid.UUID()))

    assert isinstance(region, Region)


@pytest.mark
def test_create_region_with_invalid_iso():
    invalid_iso = "R1U-M3OS"
    with pytest.raises(ValueError) as excinfo:
        Region.create(iso=invalid_iso, name="Москва", name_english="Moscow", country_id=EntityId(uuid.UUID()))

    assert f"'{invalid_iso}' is not a valid ISO code." in str(excinfo.value)
