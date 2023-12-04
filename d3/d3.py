from __future__ import annotations
from dataclasses import dataclass
from typing import List
from typing import Tuple

@dataclass
class Symbol:
    symbol: str
    row: int
    column: int

    def is_gear(self) -> bool:
        return self.symbol == "*"

@dataclass
class Part:
    number: int
    row: int
    col: int

@dataclass
class Gear:
    row: int
    col: int
    parts: Tuple[Part, Part]

    def get_ratio(self) -> int:
        return self.parts[0].number * self.parts[1].number

@dataclass
class Schematic:
    symbols: List[Symbol]
    parts: List[Part]

    @staticmethod
    def parse(lines: List[str]) -> Schematic:
        parts: List[Part] = []
        symbols: List[Symbol] = []

        for row in range(0, len(lines)):
            line = lines[row]

            part_number: int = -1

            for col in range(0, len(line)):
                if line[col].isnumeric():
                    if part_number != -1:
                        part_number = part_number * 10 + int(line[col])
                    else:
                        part_number = int(line[col])

                    if col == len(line) - 1:
                        parts.append(Part(part_number, row, col - (len(str(part_number)) - 1)))
                        part_number = -1

                elif line[col] == ".":
                    if part_number != -1:
                        parts.append(Part(part_number, row, col - len(str(part_number))))
                        part_number = -1
                else:
                    if part_number != -1:
                        parts.append(Part(part_number, row, col - len(str(part_number))))
                        part_number = -1

                    symbols.append(Symbol(line[col], row, col))

        return Schematic(symbols, parts)

    def __is_adjacent_to_symbol(self, part: Part) -> bool:
        for symbol in self.symbols:
            if self.__are_adjacent(symbol, part):
                return True

        return False
    def find_part_numbers(self) -> List[Part]:
        adjacent_parts: List[Part] = []

        for part in self.parts:
            if self.__is_adjacent_to_symbol(part):
                adjacent_parts.append(part)

        return adjacent_parts

    @staticmethod
    def __are_adjacent(symbol: Symbol, part: Part):
        part_col_start = part.col
        part_col_end = part.col + len(str(part.number)) - 1

        return (symbol.row >= part.row - 1 and
                symbol.row <= part.row + 1 and
                symbol.column >= part_col_start - 1 and
                symbol.column <= part_col_end + 1)

    def find_gears(self) -> List[Gear]:
        gears: List[Gear] = []

        for symbol in self.symbols:
            if symbol.is_gear():
                adjacent_parts: List[Part] = []

                for part in self.parts:
                    if self.__are_adjacent(symbol, part):
                        adjacent_parts.append(part)

                if len(adjacent_parts) == 2:
                    gears.append(Gear(symbol.row, symbol.column, (adjacent_parts[0], adjacent_parts[1])))

        return gears

if __name__ == "__main__":
    with open("input.txt") as data:
        schematic: Schematic = Schematic.parse(data.read().splitlines())
        # parts: List[Part] = schematic.find_part_numbers()
        # print(sum(map(lambda part: part.number, parts)))

        gears = schematic.find_gears()
        print(sum(map(lambda gear: gear.get_ratio(), gears)))


