from dataclasses import dataclass

from src.application.dto.airports.create_dto import CreateAirportDTO
from src.application.usecases.airports.import_airports.load_data import AirportLoadData
from src.entities.location.city.city import City
from src.entities.location.country.country import Country
from src.entities.location.country.iso import ISOCode as ISOCountryCode
from src.entities.location.region.iso import ISOCode as ISORegionCode
from src.entities.location.region.region import Region


@dataclass
class AirportsAdapterResponse:
    invalid: int
    airports: list[CreateAirportDTO]


class AirportLoadDataToCreateDTOAdapter:
    async def execute(
        self,
        data: list[AirportLoadData],
        countries_dict: dict[ISOCountryCode, Country],
        regions_dict: dict[ISORegionCode, Region],
        cities_dict: dict[str, City],
    ) -> AirportsAdapterResponse:
        airports = []
        invalid = 0

        for load_data in data:
            country = countries_dict.get(load_data.country_iso)  # type: ignore
            region = regions_dict.get(load_data.region_iso)  # type: ignore
            city = cities_dict.get(load_data.municipality)  # type: ignore

            if country is None or region is None or city is None:
                invalid += 1
                continue

            try:
                airport = CreateAirportDTO(
                    name=load_data.name,
                    continent=load_data.continent,
                    country_id=country.id.value,
                    region_id=region.id.value,
                    city_id=city.id.value,
                    scheduled_service=load_data.scheduled_service,
                    icao=load_data.icao,
                    iata=load_data.iata,
                    gps_code=load_data.gps_code,
                    name_russian=load_data.name_russian,
                )

                airports.append(airport)
            except ValueError as e:
                invalid += 1
                print(f"Error while building Create Airport DTO: {e}")

        return AirportsAdapterResponse(invalid=invalid, airports=airports)
