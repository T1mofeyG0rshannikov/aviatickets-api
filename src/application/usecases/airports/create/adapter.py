from dataclasses import dataclass

from src.application.dto.airports.csv_data import CsvAirportData
from src.entities.airport.airport import Airport
from src.entities.airport.iata_code import IATACode
from src.entities.airport.icao_code import ICAOCode
from src.entities.location.city.city import City
from src.entities.location.country.country import Country
from src.entities.location.country.iso import ISOCode as ISOCountryCode
from src.entities.location.region.iso import ISOCode as ISORegionCode
from src.entities.location.region.region import Region


@dataclass
class AirportsCsvToAirportAdapterResponse:
    invalid: int
    airports: list[Airport]


class CsvToAirportAdapter:
    async def execute(
        self,
        data: list[CsvAirportData],
        countries_dict: dict[ISOCountryCode, Country],
        regions_dict: dict[ISORegionCode, Region],
        cities_dict: dict[str, City],
    ) -> AirportsCsvToAirportAdapterResponse:
        airports = []
        invalid = 0

        for csv_data in data:
            country = countries_dict.get(csv_data.iso_country)
            region = regions_dict.get(csv_data.iso_region)
            city = cities_dict.get(csv_data.municipality)

            try:
                airport = Airport.create(
                    name=csv_data.name,
                    continent=csv_data.continent,
                    country_id=country.id if country else None,
                    region_id=region.id if region else None,
                    city_id=city.id if city else None,
                    scheduled_service=csv_data.scheduled_service,
                    icao=ICAOCode(csv_data.icao),
                    iata=IATACode(csv_data.iata),
                    gps_code=csv_data.gps_code,
                    name_russian=csv_data.name_russian,
                )

                airports.append(airport)
            except ValueError as e:
                invalid += 1
                print(f"Error while building Airport: {e}")

        return AirportsCsvToAirportAdapterResponse(invalid=invalid, airports=airports)
