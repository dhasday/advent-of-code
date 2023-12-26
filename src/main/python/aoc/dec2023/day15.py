import dataclasses
import re
from collections import defaultdict

from aoc.common.day_solver import DaySolver

INSTRUCTION_REGEX = re.compile(r'([a-z]+)([-=])(\d*)')


@dataclasses.dataclass
class Lens:
    name: str
    focal_length: int

    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return f'{self.name} {self.focal_length}'


class Day15Solver(DaySolver):
    year = 2023
    day = 15

    def solve_puzzle_one(self):
        return sum(self._hash_sequence(seq) for seq in self.load_only_input_line().split(','))

    def solve_puzzle_two(self):
        line = self.load_only_input_line()

        boxes = defaultdict(list)
        for sequence in line.split(','):
            name, action, value = INSTRUCTION_REGEX.match(sequence).groups()

            box_num = self._hash_sequence(name)
            current_box = boxes[box_num]
            value = 0 if value == '' else int(value)

            lens = Lens(name, value)

            if action == '-':
                if lens in current_box:
                    current_box.remove(lens)
            elif action == '=':
                try:
                    lens_index = current_box.index(lens)
                    current_box[lens_index] = lens
                except ValueError:
                    current_box.append(lens)

        total = 0
        for box, lenses in boxes.items():
            for idx, lens in enumerate(lenses):
                total += (box + 1) * (idx + 1) * lens.focal_length
        return total

    def _hash_sequence(self, sequence):
        current = 0
        for char in sequence:
            current += ord(char)
            current *= 17
            current %= 256
        return current
