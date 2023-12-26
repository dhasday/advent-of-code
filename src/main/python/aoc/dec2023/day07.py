from collections import Counter

from aoc.common.day_solver import DaySolver

FIVE_OF_A_KIND = 70
FOUR_OF_A_KIND = 60
FULL_HOUSE = 50
THREE_OF_A_KIND = 40
TWO_PAIR = 30
ONE_PAIR = 20
HIGH_CARD = 10

RANK_ORDER_DEFAULT = {
    'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10,
    '9': 9, '8': 8, '7': 7, '6': 6, '5': 5,
    '4': 4, '3': 3, '2': 2,
}
RANK_ORDER_WILDS = {
    'A': 14, 'K': 13, 'Q': 12, 'T': 10,
    '9': 9, '8': 8, '7': 7, '6': 6, '5': 5,
    '4': 4, '3': 3, '2': 2, 'J': 1,
}


class Hand:
    cards: str
    bid: int

    def __init__(self, cards, bid, with_wilds=False):
        self.cards = cards
        self.bid = int(bid)

        if with_wilds:
            self.rank_cards = [RANK_ORDER_WILDS[card] for card in cards]
        else:
            self.rank_cards = [RANK_ORDER_DEFAULT[card] for card in cards]

        if with_wilds:
            self.hand_type = self._determine_hand_type_with_wilds()
        else:
            self.hand_type = self._determine_hand_type()

    def _determine_hand_type(self):
        two_most_common = Counter(self.rank_cards).most_common(2)

        most_common_count = two_most_common[0][1]
        if len(two_most_common) == 1:
            second_common_count = 0
        else:
            second_common_count = two_most_common[1][1]

        return self._rank_hand(most_common_count, second_common_count)

    def _determine_hand_type_with_wilds(self):
        counter = Counter(self.rank_cards)
        num_wilds = counter.pop(1) if 1 in counter else 0

        two_most_common = counter.most_common(2)
        most_common_count = num_wilds if num_wilds == 5 else two_most_common[0][1] + num_wilds
        if len(two_most_common) < 2:
            second_common_count = 0
        else:
            second_common_count = two_most_common[1][1]

        return self._rank_hand(most_common_count, second_common_count)

    def _rank_hand(self, most_common_count, second_common_count):
        if most_common_count == 5:
            return FIVE_OF_A_KIND
        if most_common_count == 4:
            return FOUR_OF_A_KIND

        if most_common_count == 3:
            if second_common_count == 2:
                return FULL_HOUSE
            else:
                return THREE_OF_A_KIND
        if most_common_count == 2:
            if second_common_count == 2:
                return TWO_PAIR
            else:
                return ONE_PAIR
        return HIGH_CARD

    def __eq__(self, other):
        return self.hand_type == other.hand_type and self.rank_cards == other.rank_cards

    def __lt__(self, other):
        if self.hand_type == other.hand_type:
            return self.rank_cards < other.rank_cards
        else:
            return self.hand_type < other.hand_type


class Day07Solver(DaySolver):
    year = 2023
    day = 7

    def setup(self):
        pass

    def solve_puzzle_one(self):
        lines = self.load_all_input_lines()

        hands = []
        for line in lines:
            hands.append(Hand(*line.split(' ')))

        return self._score_hands(hands)

    def solve_puzzle_two(self):
        lines = self.load_all_input_lines()

        hands = []
        for line in lines:
            hands.append(Hand(*line.split(' '), with_wilds=True))

        return self._score_hands(hands)

    def _score_hands(self, hands):
        hands = sorted(hands)
        total = 0
        for idx, hand in enumerate(hands, start=1):
            total += (idx * hand.bid)
        return total
