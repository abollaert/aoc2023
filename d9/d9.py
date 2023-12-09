from __future__ import annotations
from dataclasses import dataclass
from typing import List

@dataclass
class ValueHistory:
    values: List[int]
    derived: ValueHistory
    parent: ValueHistory

    @staticmethod
    def parse(line: str) -> ValueHistory:
        value_history: ValueHistory = ValueHistory([int(value) for value in line.split()], None, None)
        value_history.derive()

        return value_history

    def __derive_difference_sequence(self) -> ValueHistory:
        differences: List[int] = []

        for i in range(1, len(self.values)):
            differences.append(self.values[i] - self.values[i - 1])

        return ValueHistory(differences, None, self)

    def __is_all_zeroes(self):
        for v in self.values:
            if v != 0:
                return False

        return True

    def derive(self):
        current: ValueHistory = self
        current.derived = current.__derive_difference_sequence()

        while not current.derived.__is_all_zeroes():
            current = current.derived
            current.derived = current.__derive_difference_sequence()

    def next_value(self):
        current: ValueHistory = self

        while current.derived is not None:
            current = current.derived

        if current.__is_all_zeroes():
            current.values.append(0)
            current = current.parent

        while current.parent is not None:
            current.values.append(current.values[len(current.values) - 1] + current.derived.values[len(current.derived.values) - 1])
            current = current.parent

        current.values.append(current.values[len(current.values) - 1] + current.derived.values[len(current.derived.values) - 1])

    def previous_value(self):
        current: ValueHistory = self

        while current.derived is not None:
            current = current.derived

        if current.__is_all_zeroes():
            current.values.insert(0, 0)
            current = current.parent

        while current.parent is not None:
            current.values.insert(0, current.values[0] - current.derived.values[0])
            current = current.parent

        current.values.insert(0, current.values[0] - current.derived.values[0])

if __name__ == "__main__":
    with open("input.txt") as data_file:
        value_histories: List[ValueHistory] = []

        for line in data_file.readlines():
            value_histories.append(ValueHistory.parse(line))

        sum: int = 0

        for value_history in value_histories:
            value_history.previous_value()
            sum = sum + value_history.values[0]

        print(sum)
