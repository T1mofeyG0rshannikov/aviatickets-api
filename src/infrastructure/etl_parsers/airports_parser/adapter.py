from src.application.dto.airports.create_dto import CreateAirportDTO
from src.application.usecases.airports.create.loader import AirportsLoaderResponse
from src.entities.location.city.city import City
from src.entities.location.country.country import Country
from src.entities.location.country.iso import ISOCode as ISOCountryCode
from src.entities.location.region.iso import ISOCode as ISORegionCode
from src.entities.location.region.region import Region
from src.infrastructure.etl_parsers.airports_parser.csv_data import AirportCSVData


class CsvToAirportAdapter:
    async def execute(
        self,
        data: list[AirportCSVData],
        countries_dict: dict[ISOCountryCode, Country],
        regions_dict: dict[ISORegionCode, Region],
        cities_dict: dict[str, City],
    ) -> AirportsLoaderResponse:
        airports = []
        invalid = 0

        for csv_data in data:
            country = countries_dict.get(csv_data.iso_country)  # type: ignore
            region = regions_dict.get(csv_data.iso_region)  # type: ignore
            city = cities_dict.get(csv_data.municipality)  # type: ignore

            try:
                airport = CreateAirportDTO(
                    name=csv_data.name,
                    continent=csv_data.continent,
                    country_id=country.id.value if country else None,
                    region_id=region.id.value if region else None,
                    city_id=city.id.value if city else None,
                    scheduled_service=csv_data.scheduled_service,
                    icao=csv_data.icao,
                    iata=csv_data.iata,
                    gps_code=csv_data.gps_code,
                    name_russian=csv_data.name_russian,
                )

                airports.append(airport)
            except ValueError as e:
                invalid += 1
                print(f"Error while building Create Airport DTO: {e}")

        return AirportsLoaderResponse(invalid=invalid, airports=airports)
