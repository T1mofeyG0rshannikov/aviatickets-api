import pytest

from src.entities.location.region.exceptions import InvalidRegionISOCode
from src.entities.location.region.iso import ISOCode
from src.entities.location.region.region import Region
from src.entities.value_objects.entity_id import EntityId


def test_create_region():
    region = Region.create(iso="RU-MOS", name="Москва", name_english="Moscow", country_id=EntityId.generate())

    assert isinstance(region, Region)


def test_create_region_with_invalid_iso():
    invalid_iso = "R1U-M3OS"
    with pytest.raises(InvalidRegionISOCode) as excinfo:
        Region.create(iso=ISOCode(invalid_iso), name="Москва", name_english="Moscow", country_id=EntityId.generate())

    assert f"'{invalid_iso}' is not a valid ISO code." in str(excinfo.value)
