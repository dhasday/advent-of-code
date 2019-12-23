from aoc.common.day_solver import DaySolver
from aoc.dec2019.common.intcode_processor import IntcodeProcessor


class Day19Solver(DaySolver):
    year = 2019
    day = 19

    def solve_puzzle_one(self):
        line = self.load_only_input_line()

        affected = set()
        min_previous = 0
        processor = IntcodeProcessor(line)
        for x in range(50):
            min_next = None
            found = False
            for y in range(min_previous, 50):
                output = self._test_pos(processor, x, y)
                if output == 1:
                    found = True
                    affected.add((x, y))
                    if min_next is None or min_next > y:
                        min_next = y
                elif found:
                    break
            if min_next is None:
                min_next = 0
            min_previous = min_next

        return len(affected)

    def solve_puzzle_two(self):
        line = self.load_only_input_line()

        processor = IntcodeProcessor(line)

        # Start point picked based on approx guess from first part
        min_affected = 500
        max_affected = 500
        y = 500
        while True:
            min_affected, max_affected = self._get_row_bounds(processor, y, min_affected, max_affected)
            if max_affected - min_affected > 100:
                x = max_affected - 99
                output = self._test_pos(processor, x, y + 99)
                if output == 1:
                    return x * 10000 + y
            y += 1

    def _get_row_bounds(self, processor, row, prev_min, prev_max):
        next_min = prev_min
        while True:
            output = self._test_pos(processor, next_min, row)
            if output == 1:
                break
            next_min += 1

        next_max = max(next_min, prev_max)
        while True:
            output = self._test_pos(processor, next_max, row)
            if output == 0:
                next_max -= 1
                break
            next_max += 1

        return next_min, next_max

    def _test_pos(self, processor, x, y):
        processor.reset()
        processor.input_value = x
        processor.stop_after_instruction(3)

        return processor.get_next_output(y)
