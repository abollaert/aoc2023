from __future__ import annotations
from dataclasses import dataclass
from dataclasses import field
from typing import List
from typing import Set


@dataclass(unsafe_hash=True)
class Tile:
    row: int
    col: int
    symbol: str
    start_tile: bool = field(init = False)
    on_loop: bool = field(init = False)

    def __post_init__(self):
        if self.symbol == "S":
            self.start_tile = True
        else:
            self.start_tile = False

        self.on_loop = False

    def is_start_tile(self) -> bool:
        return self.start_tile

@dataclass
class Grid:
    tiles: List[List[Tile]]

    @staticmethod
    def parse(lines: List[str]) -> Grid:
        tiles: List[List[Tile]] = []

        for i in range(0, len(lines)):
            line: str = lines[i].strip()

            row: List[Tile] = []

            for j in range(0, len(line)):
                symbol: str = line[j]

                row.append(Tile(i, j, symbol))

            tiles.append(row)

        grid: Grid = Grid(tiles)

        for tile in grid.get_start_tiles():
            tile.symbol = grid.determine_node_type_for_starting_point(tile)

        return grid

    def get_start_tiles(self):
        start_tiles: List[Tile] = []

        for row in self.tiles:
            for tile in row:
                if tile.is_start_tile():
                    start_tiles.append(tile)

        return start_tiles

    def __get_tile(self, row: int, col: int):
        return self.tiles[row][col]

    def get_neighbors(self, tile: Tile) -> List[Tile]:
        if tile.symbol == ".":
            return []
        elif tile.symbol == "|":
            return [ self.__get_tile(tile.row - 1, tile.col), self.__get_tile(tile.row + 1, tile.col) ]
        elif tile.symbol == "-":
            return [ self.__get_tile(tile.row, tile.col - 1), self.__get_tile(tile.row, tile.col + 1) ]
        elif tile.symbol == "L":
            return [ self.__get_tile(tile.row - 1, tile.col), self.__get_tile(tile.row, tile.col + 1) ]
        elif tile.symbol == "J":
            return [ self.__get_tile(tile.row - 1, tile.col), self.__get_tile(tile.row, tile.col - 1) ]
        elif tile.symbol == "F":
            return [ self.__get_tile(tile.row + 1, tile.col), self.__get_tile(tile.row, tile.col + 1) ]
        elif tile.symbol == "7":
            return [ self.__get_tile(tile.row + 1, tile.col), self.__get_tile(tile.row, tile.col - 1) ]

    def __has_pipe(self, tile):
        return tile.symbol != "."

    def __are_connected(self, tile1: Tile, tile2: Tile) -> bool:
        if tile2.row == tile1.row:
            if tile2.col == tile1.col - 1:
                return (tile2.symbol == "-" or tile2.symbol == "F" or tile2.symbol == "L" or tile2.symbol == "S") and (tile1.symbol == "-" or tile1.symbol == "7" or tile1.symbol == "J" or tile1.symbol == "S")
            elif tile2.col == tile1.col + 1:
                return (tile2.symbol == "-" or tile2.symbol == "J" or tile2.symbol == "7" or tile2.symbol == "S") and (tile1.symbol == "-" or tile1.symbol == "F" or tile1.symbol == "L" or tile1.symbol == "S")
        elif tile2.col == tile1.col:
            if tile2.row == tile1.row + 1:
                return (tile2.symbol == "|" or tile2.symbol == "J" or tile2.symbol == "L" or tile2.symbol == "S") and (tile1.symbol == "|" or tile1.symbol == "F" or tile1.symbol == "7" or tile1.symbol == "S")
            elif tile2.row == tile1.row - 1:
                return (tile2.symbol == "|" or tile2.symbol == "F" or tile2.symbol == "7" or tile2.symbol == "S") and (tile1.symbol == "|" or tile1.symbol == "J" or tile1.symbol == "L" or tile1.symbol == "S")

        return False

    def determine_node_type_for_starting_point(self, starting_point: Tile):
        north: Tile = self.__get_tile(starting_point.row - 1, starting_point.col)
        east: Tile = self.__get_tile(starting_point.row, starting_point.col + 1)
        south: Tile = self.__get_tile(starting_point.row + 1, starting_point.col)
        west: Tile = self.__get_tile(starting_point.row, starting_point.col - 1)

        if self.__are_connected(starting_point, north) and self.__are_connected(starting_point, south):
            return "|"
        elif self.__are_connected(starting_point, north) and self.__are_connected(starting_point, east):
            return "L"
        elif self.__are_connected(starting_point, north) and self.__are_connected(starting_point, west):
            return "J"
        elif self.__are_connected(starting_point, south) and self.__are_connected(starting_point, east):
            return "F"
        elif self.__are_connected(starting_point, south) and self.__are_connected(starting_point, west):
            return "7"
        elif self.__are_connected(starting_point, east) and self.__are_connected(starting_point, west):
            return "-"

    def get_loop_length(self, start_point: Tile):
        visited: Set[Tile] = set()
        length: int = 0

        current_points: List[Tile] = self.get_neighbors(start_point)

        finished: bool = False

        while not finished:
            next_tiles: List[Tile] = []

            for current_tile in current_points:
                neighbors: List[Tile] = self.get_neighbors(current_tile)

                for neighbor in neighbors:
                    if neighbor not in visited:
                        next_tiles.append(neighbor)

                visited.add(current_tile)
                current_tile.on_loop = True

            current_points = next_tiles
            length = length + 1

            finished = True

            for tile in current_points:
                if tile not in visited:
                    finished = False

        return length

    def count_inside_loop(self) -> int:
        inside_loop: int = 0

        for i in range(0, len(self.tiles)):
            count: int = 0
            up: bool = True

            row: List[Tile] = self.tiles[i]

            for j in range(0, len(row)):
                tile: Tile = row[j]

                if self.__has_pipe(tile) and tile.on_loop:
                    if tile.symbol == "7" or tile.symbol == "F" or tile.symbol == "|":
                        if up:
                            count = count + 1
                            up = False
                        else:
                            count = count - 1
                            up = True
                elif tile.on_loop == False and not tile.start_tile:
                    if count == 1:
                        inside_loop = inside_loop + 1

        return inside_loop

if __name__ == "__main__":
    with open("input.txt") as data_file:
        grid: Grid = Grid.parse(data_file.readlines())
        print(grid.get_loop_length(grid.get_start_tiles()[0]))
        print(grid.count_inside_loop())

