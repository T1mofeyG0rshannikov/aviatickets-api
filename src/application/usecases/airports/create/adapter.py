from src.application.dto.airports.csv_data import CsvAirportData
from src.entities.airport.dto import CreateAirportDTO
from src.entities.airport.iata_code import IATACode
from src.entities.airport.icao_code import ICAOCode
from src.entities.city.city import City
from src.entities.country.country import Country
from src.entities.country.iso import ISOCode as ISOCountryCode
from src.entities.region.iso import ISOCode as ISORegionCode
from src.entities.region.region import Region


class AirportsCsvToCreateDTOAdapter:
    def execute(
        self,
        data: list[CsvAirportData],
        countries_dict: dict[ISOCountryCode, Country],
        regions_dict: dict[ISORegionCode, Region],
        cities_dict: dict[str, City],
    ) -> list[CreateAirportDTO]:
        output_data = []

        for csv_data in data:
            if csv_data.iata or csv_data.icao:
                country = countries_dict.get(csv_data.iso_country)
                region = regions_dict.get(csv_data.iso_region)
                city = cities_dict.get(csv_data.municipality)

                try:
                    output_data.append(
                        CreateAirportDTO(
                            name=csv_data.name,
                            continent=csv_data.continent,
                            country_id=country.id if country else None,
                            region_id=region.id if region else None,
                            city_id=city.id if city else None,
                            scheduled_service=csv_data.scheduled_service,
                            icao=csv_data.icao,
                            iata=csv_data.iata,
                            gps_code=csv_data.gps_code,
                            name_russian=csv_data.name_russian,
                        )
                    )
                except ValueError as e:
                    print(f"Error while build CreateAirportDTO: {e}")

        return output_data
