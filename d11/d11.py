from __future__ import annotations

from dataclasses import dataclass

from typing import List
from typing import Tuple

from queue import Queue

@dataclass
class PathItem:
    row: int
    col: int
    distance: int

@dataclass
class Distance:
    g1: str
    g2: str
    distance: int

@dataclass
class Galaxy:
    name: str
    row: int
    col: int

@dataclass
class Universe:

    galaxies: List[Galaxy]
    size: Tuple[int, int]

    @staticmethod
    def parse(lines: List[str]) -> Universe:
        galaxy_index: int = 1
        galaxies: List[Galaxy] = []

        max_col: int = 0
        max_row: int = 0

        for i in range(0, len(lines)):
            line: str = lines[i].strip()

            for j in range(0, len(line)):
                if line[j] == "#":
                    galaxies.append(Galaxy(str(galaxy_index), i, j))
                    galaxy_index = galaxy_index + 1

                    if j > max_col:
                        max_col = j

                    if i > max_row:
                        max_row = i

        return Universe(galaxies, (max_row, max_col))

    def __post_init__(self):
        self.__expand_empty_rows_and_cols(999999)

    def __is_empty_row(self, row: int):
        for galaxy in self.galaxies:
            if galaxy.row == row:
                return False

        return True

    def __is_empty_col(self, col: int):
        for galaxy in self.galaxies:
            if galaxy.col == col:
                return False

        return True

    def __expand_empty_rows_and_cols(self, expansion_size: int = 1) -> None:
        print("Performing expansion.")

        empty_rows: List[int] = []
        empty_cols: List[int] = []

        for i in range(0, self.size[0]):
            empty: bool = True

            for galaxy in self.galaxies:
                if galaxy.row == i:
                    empty = False

                    break

            if empty:
                empty_rows.append(i)

        for i in range(0, self.size[1]):
            empty: bool = True

            for galaxy in self.galaxies:
                if galaxy.col == i:
                    empty = False

                    break

            if empty:
                empty_cols.append(i)

        num_rows_added: int = 0

        for row in empty_rows:
            adjusted_row: int = row + num_rows_added

            for galaxy in self.galaxies:
                if galaxy.row > adjusted_row:
                    galaxy.row = galaxy.row + expansion_size

            num_rows_added = num_rows_added + expansion_size

        num_cols_added: int = 0

        for col in empty_cols:
            adjusted_col: int = col + num_cols_added

            for galaxy in self.galaxies:
                if galaxy.col > adjusted_col:
                    galaxy.col = galaxy.col + expansion_size

            num_cols_added = num_cols_added + expansion_size

        max_row: int = 0
        max_col: int = 0

        for galaxy in self.galaxies:
            if galaxy.row > max_row:
                max_row = galaxy.row

            if galaxy.col > max_col:
                 max_col = galaxy.col

        self.size = (max_row, max_col)

    def euclidian(self, galaxy1: Galaxy, galaxy2: Galaxy) -> int:
        return abs(galaxy1.row - galaxy2.row) + abs(galaxy1.col - galaxy2.col)

if __name__ == "__main__":
    with open("input.txt") as data_file:
        universe: Universe = Universe.parse(data_file.readlines())
        galaxies: List[Galaxy] = universe.galaxies

        print("Number of galaxies : %i" % len(galaxies))

        distances: List[Distance] = []
        distances_calculated: set = set()

        for galaxy1 in galaxies:
            for galaxy2 in galaxies:
                if galaxy1.name != galaxy2.name:
                    galaxy_tuple = tuple(sorted((galaxy1.name, galaxy2.name)))

                    if galaxy_tuple not in distances_calculated:
                        calculated_distance: int = universe.euclidian(galaxy1, galaxy2)

                        distances.append(Distance(galaxy1.name, galaxy2.name, calculated_distance))
                        distances_calculated.add(galaxy_tuple)

        print(distances)
        print(sum(map(lambda d: d.distance, distances)))
