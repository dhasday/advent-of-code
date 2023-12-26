from aoc.common import helpers
from aoc.common.day_solver import DaySolver


class Day09Solver(DaySolver):
    year = 2023
    day = 9

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        ans_one = 0
        ans_two = 0
        lengths = set()
        for line in lines:
            sequence = [int(v) for v in helpers.ALL_NUMBERS_REGEX.findall(line)]
            lengths.add(len(sequence))

            cur_layer = sequence

            is_odd = len(sequence) % 2 == 1
            first_seq = list(sequence[0:1])
            next_value = sequence[-1]
            while any(v for v in cur_layer if v != 0):
                next_layer = []
                for idx in range(len(cur_layer) - 1):
                    next_layer.append(cur_layer[idx + 1] - cur_layer[idx])

                cur_layer = next_layer
                first_seq.append(cur_layer[0])
                next_value += cur_layer[-1]
                is_odd = not is_odd

            prev_value = 0
            while first_seq:
                prev_value = first_seq.pop() - prev_value

            ans_one += next_value
            ans_two += prev_value

        return ans_one, ans_two
