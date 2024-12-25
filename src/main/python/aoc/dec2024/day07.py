from aoc.common.day_solver import DaySolver


class Day07Solver(DaySolver):
    year = 2024
    day = 7

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        total_p1 = 0
        total_p2 = 0
        for line in lines:
            target, values = line.split(': ')

            target = int(target)
            nums = [int(v) for v in values.split(' ')]

            p1_valid, p2_valid = self._is_valid(target, nums)
            if p1_valid:
                total_p1 += target
            if p2_valid:
                total_p2 += target

        return total_p1, total_p2

    def _is_valid(self, target, nums):
        current_values = set()
        current_values.add((nums[0], False))
        for num in nums[1:]:
            next_values = set()
            for cur_val, used_concat in current_values:
                next_add = cur_val + num
                if next_add <= target:
                    next_values.add((next_add, used_concat))

                next_mult = cur_val * num
                if next_mult <= target:
                    next_values.add((next_mult, used_concat))

                next_concat = int(str(cur_val) + str(num))
                if next_concat <= target:
                    next_values.add((next_concat, True))
            current_values = next_values

        p1_valid = (target, False) in current_values
        p2_valid = p1_valid or (target, True) in current_values
        return p1_valid, p2_valid
