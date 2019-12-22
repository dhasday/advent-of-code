import math
import re
from collections import deque, defaultdict
from functools import reduce
from itertools import islice, cycle

from aoc.common.a_star_search import AStarSearch
from aoc.common.breadth_first_search import BreadthFirstSearch
from aoc.common.day_solver import DaySolver
from aoc.common.dijkstra_search import DijkstraSearch
from aoc.common.helpers import ALL_NUMBERS_REGEX, STANDARD_DIRECTIONS
from aoc.dec2019.common.intcode_processor import IntcodeProcessor


INS_DEAL_NEW_STACK = 'deal into new stack'
INS_CUT = 'cut '
INS_DEAL_INCREMENT = 'deal with increment '


class Day22Solver(DaySolver):
    year = 2019
    day = 22

    class Deck(object):

        def __init__(self, size):
            self.cards = list(range(size))
            self.num_cards = size

        def __getitem__(self, key):
            return self.cards[key]

        def __setitem__(self, key, value):
            self.cards[key] = value

        def __str__(self):
            return str(self.cards)

        def do_shuffle(self, instruction):
            instruction.split(' ')
            if instruction == INS_DEAL_NEW_STACK:
                self.deal_new_stack()
            elif instruction.startswith(INS_DEAL_INCREMENT):
                self.deal_with_increment(int(instruction[20:]))
            elif instruction.startswith(INS_CUT):
                self.cut_deck(int(instruction[4:]))
            else:
                raise Exception('Unmatched instruction: ' + instruction)

        def deal_new_stack(self):
            self.cards = self.cards[::-1]

        def cut_deck(self, index):
            self.cards = self.cards[index:] + self.cards[:index]

        def deal_with_increment(self, increment):
            ptr = 0
            new_cards = [0] * self.num_cards
            for card in self.cards:
                new_cards[ptr % self.num_cards] = card
                ptr += increment
            self.cards = new_cards

    def solve_puzzle_one(self):
        card_count = 10007

        deck = self.Deck(card_count)

        lines = self._load_all_input_lines()
        for line in lines:
            deck.do_shuffle(line)

        idx = 0
        while True:
            if deck[idx] == 2019:
                return idx
            idx += 1

    def solve_puzzle_two(self):
        # TODO: This won't run in any reasonable amount of time
        return None

        card_count = 119315717514047
        num_shuffles = 101741582076661

        deck = self.Deck(card_count)

        lines = self._load_all_input_lines()
        for _ in range(num_shuffles):
            import pdb; pdb.set_trace()
            for line in lines:
                deck.do_shuffle(line)

        return deck[2020]
