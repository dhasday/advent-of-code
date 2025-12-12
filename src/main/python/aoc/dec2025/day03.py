from aoc.common.day_solver import DaySolver


class Day03Solver(DaySolver):
    year = 2025
    day = 3

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        total_joltage_p1 = 0
        total_joltage_p2 = 0
        for line in lines:
            total_joltage_p1 += self._find_highest_joltage(line, 2)
            total_joltage_p2 += self._find_highest_joltage(line, 12)

        return total_joltage_p1, total_joltage_p2

    def _find_highest_joltage(self, line, num_to_select, max_value=9):
        # If there aren't enough options left, fail to find joltage
        if len(line) < num_to_select:
            return -1
        # If there's no more to select, we're done
        if num_to_select == 0:
            return 0

        # Loop from max_value -> 1 and select the first highest option that results in a valid joltage
        for val in range(max_value, 0, -1):
            idx = line.find(str(val))
            if idx != -1:
                total = self._find_highest_joltage(line[idx + 1:], num_to_select - 1, max_value)
                if total >= 0:
                    return (val * (10 ** (num_to_select - 1))) + total

        return -1
