from __future__ import annotations

import functools
from dataclasses import dataclass
from typing import List

@dataclass
class Sample:

    num_blue: int
    num_red: int
    num_green: int

    @staticmethod
    def parse(sample_data: str) -> Sample:
        parts = sample_data.split(",")

        num_blue: int = 0
        num_red: int = 0
        num_green: int = 0

        for part in parts:
            single_parts = part.strip().split(" ")

            number = int(single_parts[0])
            color = single_parts[1]

            if color == "blue":
                num_blue = number
            elif color == "green":
                num_green = number
            elif color == "red":
                num_red = number

        return Sample(num_blue, num_red, num_green)

@dataclass
class Game:

    name: str
    samples: List[Sample]

    @staticmethod
    def parse(line: str) -> Game:
        parts = line.split(":")
        game_name: str = parts[0]
        samples_parts = parts[1].split(";")

        samples: List[Sample] = []

        for sample_part in samples_parts:
            samples.append(Sample.parse(sample_part.strip()))

        return Game(game_name,
                    samples)

    def is_possible(self, bag: Bag):
        for sample in self.samples:
            if sample.num_red > bag.num_red or sample.num_blue > bag.num_blue or sample.num_green > bag.num_green:
                return False

        return True

    def game_id(self):
        return int(self.name.split(" ")[1])

    def power(self):
        min_red: int = 0
        min_blue: int = 0
        min_green: int = 0

        for sample in self.samples:
            if sample.num_green > min_green:
                min_green = sample.num_green

            if sample.num_red > min_red:
                min_red = sample.num_red

            if sample.num_blue > min_blue:
                min_blue = sample.num_blue


        power = min_red * min_green * min_blue

        print("Game %s : Red %d, blue %d, green %d -> power %d" % (self.name, min_red, min_blue, min_green, power))

        return power

@dataclass
class Bag:
    num_red: int
    num_blue: int
    num_green: int


if __name__ == "__main__":
    with open("input.txt") as data_file:
        games = [Game.parse(line.strip()) for line in data_file]

        bag = Bag(12, 14, 13)

        # possible_games = filter(lambda game: game.is_possible(bag), games)

        sum = sum(map(lambda game: game.power(), games))

        print(sum)

