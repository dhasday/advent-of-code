import dataclasses

from aoc.common import helpers
from aoc.common.day_solver import DaySolver


class Card:
    def __init__(self, num_matches):
        self.num_matches = num_matches
        self.base_score = 2 ** (num_matches - 1) if num_matches else 0
        self.count = 1


class Day04Solver(DaySolver):
    year = 2023
    day = 4

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        results = []
        ans_one = 0
        for line in lines:
            card = Card(self._score_card(line))
            results.append(card)
            ans_one += card.base_score

        ans_two = 0
        for idx, result in enumerate(results):
            for i in range(idx + 1, idx + result.num_matches + 1):
                results[i].count += result.count
            ans_two += result.count

        return ans_one, ans_two

    def _score_card(self, card):
        [winners, numbers] = card.split(':')[1].split('|')
        winning_nums = set(helpers.ALL_DIGITS_REGEX.findall(winners))
        card_nums = helpers.ALL_DIGITS_REGEX.findall(numbers)

        match_count = 0
        for card_num in card_nums:
            if card_num in winning_nums:
                match_count += 1

        return match_count
