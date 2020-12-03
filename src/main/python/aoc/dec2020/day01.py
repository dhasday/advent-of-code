from aoc.common.day_solver import DaySolver


class Day01Solver(DaySolver):
    year = 2020
    day = 1

    def solve_puzzle_one(self):
        lines = self.load_all_input_lines()

        values = [int(v) for v in lines]
        num = len(values)

        for x in range(num):
            val_1 = values[x]
            for y in range(num):
                val_2 = values[y]
                if val_1 + val_2 == 2020:
                    return val_1 * val_2

        return 'ERROR'

    def solve_puzzle_two(self):
        lines = self.load_all_input_lines()

        values = [int(v) for v in lines]
        num = len(values)

        for x in range(num):
            val_1 = values[x]
            for y in range(num):
                val_2 = values[y]
                intermediate_sum = val_1 + val_2
                if intermediate_sum >= 2020:
                    continue
                for z in range(num):
                    val_3 = values[z]
                    if intermediate_sum + val_3 == 2020:
                        return val_1 * val_2 * val_3

        return 'ERROR'
