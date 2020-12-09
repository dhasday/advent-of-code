from aoc.common.day_solver import DaySolver


class Day09Solver(DaySolver):
    year = 2020
    day = 9

    def solve_puzzles(self):
        values = [int(line) for line in self.load_all_input_lines()]

        ans_one = self._find_first_invalid_value(values)
        ans_two = self._find_sum_range(values, ans_one)

        return ans_one, ans_two

    def _find_first_invalid_value(self, values):
        for i in range(25, len(values)):
            preamble = values[i - 25: i]
            target = values[i]

            if not self._matches_preamble(preamble, target):
                return target

        raise Exception('Found no invalid values')

    def _matches_preamble(self, preamble, target):
        for x in preamble:
            for y in preamble:
                if x != y and x + y == target:
                    return True
        return False

    def _find_sum_range(self, values, target):
        min_idx = 0
        max_idx = 0
        cur_total = 0
        for i in range(len(values)):
            cur_total += values[i]
            max_idx += 1

            if cur_total > target:
                while cur_total > target:
                    cur_total -= values[min_idx]
                    min_idx += 1

            if cur_total == target:
                sum_range = values[min_idx:max_idx]
                return min(sum_range) + max(sum_range)

        raise Exception('No matching continuous set')
