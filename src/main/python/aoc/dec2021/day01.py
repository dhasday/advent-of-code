from aoc.common.day_solver import DaySolver


class Day01Solver(DaySolver):
    year = 2021
    day = 1

    def solve_puzzle_one(self):
        lines = self.load_all_input_lines()

        prev_val = None
        count = 0
        for line in lines:
            val = int(line)
            if prev_val and val > prev_val:
                count += 1
            prev_val = val

        return count

    def solve_puzzle_two(self):
        values = [int(v) for v in self.load_all_input_lines()]

        count = 0

        prev_2 = values[1]
        prev_3 = values[2]
        prev_total = values[0] + prev_2 + prev_2
        for i in values[3:]:
            new_total = prev_2 + prev_3 + i
            if new_total > prev_total:
                count += 1
            prev_2 = prev_3
            prev_3 = i
            prev_total = new_total

        return count
