import pytest

from src.application.usecases.country.persist_countries import PersistCountries
from src.infrastructure.persistence.etl_importers.country_importer import (
    CountryImporter,
)


@pytest.fixture
def persist_countries(importer: CountryImporter) -> PersistCountries:
    return PersistCountries(importer)
