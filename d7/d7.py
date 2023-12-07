from __future__ import annotations
from dataclasses import dataclass
from dataclasses import field
from typing import List
from typing import Dict
from functools import cmp_to_key

@dataclass(eq = True, frozen = True)
class Card:
    symbol: str
    value: int

    @staticmethod
    def for_symbol(symbol: str) -> Card:
        if symbol.isnumeric():
            return Card(symbol, int(symbol) - 1)
        else:
            if symbol == "T":
                return Card(symbol, 9)
            if symbol == "J":
                return Card(symbol, 10)
            elif symbol == "Q":
                return Card(symbol, 11)
            elif symbol == "K":
                return Card(symbol, 12)
            elif symbol == "A":
                return Card(symbol, 13)

        return None

@dataclass
class Hand:
    cards: List[Card]
    bid: int
    distribution: Dict[Card, int] = field(init=False)

    def __post_init__(self):
        self.distribution = self.__get_card_distribution()

    @staticmethod
    def parse_line( line: str) -> Hand:
        parts: List[str] = line.split()

        cards: List[Card] = []
        bid: int = int(parts[1].strip())

        for card in parts[0]:
            cards.append(Card.for_symbol(card))

        return Hand(cards, bid)

    def __is_five_of_a_kind(self) -> bool:
        return self.__has_five_of_a_kind()

    def __is_four_of_a_kind(self) -> bool:
        return self.__has_four_of_a_kind()

    def __is_full_house(self) -> bool:
        return self.__get_number_of_pairs() == 1 and self.__get_number_of_triplets() == 1

    def __is_triplet(self) -> bool:
        return self.__get_number_of_triplets() == 1 and self.__get_number_of_pairs() == 0

    def __is_double_pair(self) -> bool:
        return self.__get_number_of_pairs() == 2

    def __is_single_pair(self) -> bool:
        return self.__get_number_of_pairs() == 1 and self.__get_number_of_triplets() == 0 and not self.__is_four_of_a_kind()

    def __get_number_of_pairs(self) -> int:
        num_pairs: int = 0

        for card in self.distribution.keys():
            if self.distribution[card] == 2:
                num_pairs = num_pairs + 1

        return num_pairs

    def __get_number_of_triplets(self) -> int:
        num_triplets: int = 0

        for card in self.distribution.keys():
            if self.distribution[card] == 3:
                num_triplets = num_triplets + 1

        return num_triplets

    def __has_four_of_a_kind(self) -> bool:
        return 4 in self.distribution.values()

    def __has_five_of_a_kind(self) -> bool:
        return 5 in self.distribution.values()

    def __get_card_distribution(self) -> Dict[Card, int]:
        card_distribution: Dict[Card, int] = {}

        for card in self.cards:
            if card not in card_distribution.keys():
                card_distribution[card] = 1
            else:
                card_distribution[card] = card_distribution[card] + 1

        return card_distribution

    def base_score(self):
        score: int = 0

        if self.__is_single_pair():
            score = 1
        elif self.__is_double_pair():
            score = 2
        elif self.__is_triplet():
            score = 3
        elif self.__is_full_house():
            score = 4
        elif self.__is_four_of_a_kind():
            score = 5
        elif self.__is_five_of_a_kind():
            score = 6

        return score

    def is_higher_than(self, other_hand: Hand):
        for i in range(0, len(self.cards)):
            if self.cards[i].value > other_hand.cards[i].value:
                return True
            elif other_hand.cards[i].value > self.cards[i].value:
                return False

        return True

def compare_hands(hand1: Hand, hand2: Hand):
    score1: int = hand1.base_score()
    score2: int = hand2.base_score()

    if score1 > score2:
        return 1
    elif score2 > score1:
        return -1
    else:
        if hand1.is_higher_than(hand2):
            return 1
        else:
            return -1

if __name__ == "__main__":
    hands: List[Hand] = []

    with open("input.txt") as data_file:
        for line in data_file.readlines():
            hands.append(Hand.parse_line(line))

    hands.sort(reverse = False, key = cmp_to_key(compare_hands))

    print(hands)

    winnings = 0

    for i in range(0, len(hands)):
        print("%d * %d" % ((i+1), hands[i].bid))
        winnings = winnings + (i + 1) * hands[i].bid

    print(winnings)





