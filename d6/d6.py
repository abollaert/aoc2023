from dataclasses import dataclass
from typing import List

@dataclass
class RaceRecord:
    time_allowed_ms: int
    distance_traveled: int

def parse_data(lines: List[str]) -> RaceRecord:
    time: int = 0
    distance: int = 0

    for i in range(0, 2):
        data: int = int(lines[i].strip().split(":")[1].strip().replace(" ", ""))

        if i == 0:
            time = data
        else:
            distance = data

    return RaceRecord(time, distance)

def get_number_of_ways_to_win(race_record: RaceRecord) -> int:
    number_of_ways_to_win: int = 0

    for i in range(0, race_record.time_allowed_ms):
        distance_traveled: int = (race_record.time_allowed_ms - i) * i

        if distance_traveled > race_record.distance_traveled:
            number_of_ways_to_win = number_of_ways_to_win + 1

    return number_of_ways_to_win

if __name__ == "__main__":
    with open("input.txt") as data_file:
        race_record: RaceRecord = parse_data(data_file.readlines())
        print(race_record)
        print(get_number_of_ways_to_win(race_record))