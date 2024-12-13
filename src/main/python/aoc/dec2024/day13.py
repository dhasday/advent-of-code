from aoc.common import helpers
from aoc.common.day_solver import DaySolver


P2_OFFSET = 10_000_000_000_000
TOKENS_A = 3
TOKENS_B = 1

class Day13Solver(DaySolver):
    year = 2024
    day = 13

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        total_cost_p1 = 0
        total_cost_p2 = 0

        for i in range(0, len(lines), 4):
            ax, ay = helpers.parse_all_numbers(lines[i])
            bx, by = helpers.parse_all_numbers(lines[i + 1])
            tx, ty = helpers.parse_all_numbers(lines[i + 2])

            cost_p1 = self._solve_linear(ax, ay, bx, by, tx, ty)
            if cost_p1 is not None:
                total_cost_p1 += cost_p1[0] * TOKENS_A + cost_p1[1] * TOKENS_B

            cost_p2 = self._solve_linear(ax, ay, bx, by, tx + P2_OFFSET, ty + P2_OFFSET)
            if cost_p2 is not None:
                total_cost_p2 += cost_p2[0] * TOKENS_A + cost_p2[1] * TOKENS_B

        return total_cost_p1, total_cost_p2

    def _solve_linear(self, ax, ay, bx, by, tx, ty):
        det = ax * by - ay * bx
        if det == 0:
            # If slopes are equal, then there are 0 or infinite intersections, so ignore
            return None

        num_a, rem_a = divmod(tx * by - ty * bx, det)
        num_b, rem_b = divmod(ax * ty - ay * tx, det)

        # We only want whole number solutions, so ignore if there's a remainder
        if rem_a != 0 or rem_b != 0:
            return None

        return num_a, num_b


Day13Solver().print_results()