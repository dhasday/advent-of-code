from aoc.common.day_solver import DaySolver


class Day02Solver(DaySolver):
    year = 2024
    day = 2

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        safe_p1 = 0
        safe_p2 = 0
        for line in lines:
            values = [int(v) for v in line.split(' ')]

            if self._check_safe_p1(values):
                safe_p1 += 1
                safe_p2 += 1
            elif self._check_safe_p2(values):
                safe_p2 += 1

        return safe_p1, safe_p2

    def _check_safe_p1(self, values):
        v1 = values[0]
        v2 = values[1]

        is_asc = v1 < v2

        prev = v1
        for v in values[1:]:
            diff = v - prev
            if is_asc:
                if diff < 1 or diff > 3:
                    return False
            else:
                if diff > -1 or diff < -3:
                    return False

            prev = v
        return True

    def _check_safe_p2(self, values):
        for i in range(len(values)):
            test = values[:i] + values[i + 1:]
            if self._check_safe_p1(test):
                return True
        return False


Day02Solver().print_results()
