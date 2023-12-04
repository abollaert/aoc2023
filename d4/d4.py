from __future__ import annotations
from dataclasses import dataclass
from typing import Set
from typing import List

@dataclass
class Card:
    id: int
    winning_numbers: Set[int]
    my_numbers: Set[int]
    number_owned: int
    number_of_winning_numbers: int

    @staticmethod
    def from_line(line: str) -> Card:
        parts: List[str] = line.split(":")
        card_id: int = int(parts[0].split()[1])

        parts = parts[1].split("|")

        winning_numbers: Set[int] = set(map(lambda s: int(s.strip()), parts[0].split()))
        my_numbers: Set[int] = set(map(lambda s: int(s.strip()), parts[1].split()))

        return Card(card_id, winning_numbers, my_numbers, 1, -1)

    def add_copy(self):
        self.number_owned = self.number_owned + 1

    def get_number_of_winning_numbers(self):
        if self.number_of_winning_numbers == -1:
            self.number_of_winning_numbers = 0

            for number in self.my_numbers:
                if number in self.winning_numbers:
                    self.number_of_winning_numbers = self.number_of_winning_numbers + 1

        return self.number_of_winning_numbers

    def get_points(self):
        score = 0

        for number in self.my_numbers:
            if number in self.winning_numbers:
                if score == 0:
                    score = 1
                else:
                    score = score * 2

        return score

if __name__ == "__main__":
    cards: List[Card] = []

    with open("input.txt") as data_file:
        for line in data_file.readlines():
            card: Card = Card.from_line(line)
            cards.insert(card.id - 1, card)

        card_index = 0

        for i in range(0, len(cards)):
            card = cards[i]

            for j in range(0, card.number_owned):
                num_winning: int = card.get_number_of_winning_numbers()

                for k in range(0, num_winning):
                    cards[card.id + k].add_copy()

        print(sum(map(lambda c: c.number_owned, cards)))


