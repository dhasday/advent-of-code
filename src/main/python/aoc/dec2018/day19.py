import math

from aoc.common.day_solver import DaySolver
from aoc.dec2018.common.chrono_assembly import ChronoProcessor

INSTRUCTION_POINTER = 3


class Day19Solver(DaySolver):
    year = 2018
    day = 19

    # Analyzing the instructions reduced it to this:
    #
    # Initialize
    #   if R[0] == 0
    #       R[2] = 919
    #   if R[0] == 1
    #       R[2] = 10551319
    #
    # Do the operations (which is summing all the factors of the value in R[2])
    #   R[0] = 0
    #   R[4] = 1
    #   while R[4] <= R[2]:             # for 1..value
    #       R[5] = 1
    #       while R[5] <= R[2]:         # for 1..value
    #           if R[4] * R[5] == R[2]  # if factor
    #               R[0] += R[4]        #   add first factor
    #           R[5] += 1
    #       R[4] += 1

    def solve_puzzles(self):
        # return self._solve_puzzles_by_instructions()
        return self._solve_puzzles_by_simplification()

    def _solve_puzzles_by_instructions(self):
        processor = ChronoProcessor(INSTRUCTION_POINTER)
        processor.load_instructions(self.load_all_input_lines())

        # Part One
        processor.reset()
        processor.run_until_halt()
        ans_one = processor.registers[0]

        # Part Two
        processor.reset()
        processor.registers[0] = 1
        processor.run_until_halt()
        ans_two = processor.registers[0]

        return ans_one, ans_two

    def _solve_puzzles_by_simplification(self):
        part_one_val = 919
        part_two_val = 10551319

        ans_one = self._sum_of_factors(part_one_val)
        ans_two = self._sum_of_factors(part_two_val)

        return ans_one, ans_two

    def _sum_of_factors(self, value):
        factors = set()

        limit = int(math.sqrt(value))
        for i in range(1, limit):
            j, m = divmod(value, i)
            if m == 0:
                factors.add(i)
                factors.add(j)

        return sum(factors)
