from __future__ import annotations
from dataclasses import dataclass
from typing import List
from typing import Tuple

@dataclass
class Almanac:
    seeds: List[SeedRange]
    seeds_to_soil: List[Range]
    soil_to_fertilizer: List[Range]
    fertilizer_to_water: List[Range]
    water_to_light: List[Range]
    light_to_temperature: List[Range]
    temperature_to_humidity: List[Range]
    humidity_to_location: List[Range]

    @staticmethod
    def parse(data_lines: List[str]) -> Almanac:
        seeds: List[SeedRange] = []
        seeds_to_soil: List[Range] = []
        soil_to_fertilizer: List[Range] = []
        fertilizer_to_water: List[Range] = []
        water_to_light: List[Range] = []
        light_to_temperature: List[Range] = []
        temperature_to_humidity: List[Range] = []
        humidity_to_location: List[Range] = []

        current_range: List[Range] = None

        for line in data_lines:
            if line.startswith("seeds"):
                seed_input_data = list(map(lambda s: int(s), line.split(":")[1].strip().split()))

                i: int = 0

                while i < len(seed_input_data):
                    seed_range_start: int = seed_input_data[i]
                    seed_range_length: int = seed_input_data[i + 1]

                    seeds.append(SeedRange(seed_range_start, seed_range_length))

                    i += 2

            elif line.startswith("seed-to-soil map"):
                current_range = seeds_to_soil
            elif line.startswith("soil-to-fertilizer map"):
                current_range = soil_to_fertilizer
            elif line.startswith("fertilizer-to-water map"):
                current_range = fertilizer_to_water
            elif line.startswith("water-to-light map"):
                current_range = water_to_light
            elif line.startswith("light-to-temperature map"):
                current_range = light_to_temperature
            elif line.startswith("temperature-to-humidity map"):
                current_range = temperature_to_humidity
            elif line.startswith("humidity-to-location map"):
                current_range = humidity_to_location
            elif line.strip() != "":
                current_range.append(Range.parse(line))

        return Almanac(seeds,
                       seeds_to_soil,
                       soil_to_fertilizer,
                       fertilizer_to_water,
                       water_to_light,
                       light_to_temperature,
                       temperature_to_humidity,
                       humidity_to_location)

    def __find_mapped_value(self, input_value: int, ranges: List[Range]) -> int:
        for range in ranges:
            mapped_value: int = range.find_destination(input_value)

            if mapped_value != -1:
                return mapped_value

        return input_value

    def __find_mapped_value_reverse(self, input_value, ranges: List[Range]) -> int:
        for range in ranges:
            mapped_value: int = range.find_source(input_value)

            if mapped_value != -1:
                return mapped_value

        return input_value

    def find_location_for_seed(self, seed: int) -> int:
        mapped_value: int = self.__find_mapped_value(seed, self.seeds_to_soil)
        mapped_value = self.__find_mapped_value(mapped_value, self.soil_to_fertilizer)
        mapped_value = self.__find_mapped_value(mapped_value, self.fertilizer_to_water)
        mapped_value = self.__find_mapped_value(mapped_value, self.water_to_light)
        mapped_value = self.__find_mapped_value(mapped_value, self.light_to_temperature)
        mapped_value = self.__find_mapped_value(mapped_value, self.temperature_to_humidity)
        mapped_value = self.__find_mapped_value(mapped_value, self.humidity_to_location)

        return mapped_value

    def find_seed_for_location(self, location: int) -> int:
        mapped_value: int = self.__find_mapped_value_reverse(location, self.humidity_to_location)
        mapped_value = self.__find_mapped_value_reverse(mapped_value, self.temperature_to_humidity)
        mapped_value = self.__find_mapped_value_reverse(mapped_value, self.light_to_temperature)
        mapped_value = self.__find_mapped_value_reverse(mapped_value, self.water_to_light)
        mapped_value = self.__find_mapped_value_reverse(mapped_value, self.fertilizer_to_water)
        mapped_value = self.__find_mapped_value_reverse(mapped_value, self.soil_to_fertilizer)
        mapped_value = self.__find_mapped_value_reverse(mapped_value, self.seeds_to_soil)

        return mapped_value

    def find_lowest_mapped_location(self) -> int:
        for i in range(0, 0xFFFFFFFF):
            if self.__is_location_used_by_seed(i):
                return i

    def __seed_exists(self, seed: int) -> bool:
        for seed_range in self.seeds:
            if seed >= seed_range.range_start and seed < seed_range.range_start + seed_range.range_length:
                return True

        return False

    def __is_location_used_by_seed(self, location: int) -> bool:
        seed_for_location: int = self.find_seed_for_location(location)

        return self.__seed_exists(seed_for_location)

@dataclass
class SeedRange:
    range_start: int
    range_length: int

@dataclass
class Range:
    destination_range_start: int
    source_range_start: int
    range_length: int

    @staticmethod
    def parse(line: str) -> Range:
        numbers = line.split()

        return Range(int(numbers[0]),
                     int(numbers[1]),
                     int(numbers[2]))

    def find_destination(self, number: int) -> int:
        if (number >= self.source_range_start and number < self.source_range_start + self.range_length):
            offset: int = number - self.source_range_start

            return self.destination_range_start + offset

        return -1

    def find_source(self, number: int) -> int:
        if (number >= self.destination_range_start and number < self.destination_range_start + self.range_length):
            offset: int = number - self.destination_range_start

            return self.source_range_start + offset

        return -1

if __name__ == "__main__":
    with open("input.txt") as data_file:
        print("Loading data.")

        almanac: Almanac = Almanac.parse(data_file.readlines())

        lowest_location: int = -1

        print("Finding locations.")

        print(almanac.find_lowest_mapped_location())