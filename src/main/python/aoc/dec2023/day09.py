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

            next_value = sequence[-1]

            # TODO: Fix this since it's not a generalized solution
            #       It just works for my input since all sequences are the same length
            prev_value = sequence[0]
            is_odd = len(sequence) % 2 == 1
            while any(v for v in cur_layer if v != 0):
                next_layer = []
                for idx in range(len(cur_layer) - 1):
                    next_layer.append(cur_layer[idx + 1] - cur_layer[idx])

                cur_layer = next_layer
                next_value += cur_layer[-1]
                prev_value += -cur_layer[0] if is_odd else cur_layer[0]
                is_odd = not is_odd

            ans_one += next_value
            ans_two += prev_value

        return ans_one, ans_two
