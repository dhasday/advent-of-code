from aoc.common.day_solver import DaySolver


class Day01Solver(DaySolver):
    year = 2022
    day = 1

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        cur_total = 0
        all_totals = []
        for line in lines:
            if line == '':
                all_totals.append(cur_total)
                cur_total = 0
            else:
                cur_total += int(line)
        all_totals.append(cur_total)

        all_totals = sorted(all_totals, reverse=True)

        return all_totals[0], (all_totals[0] + all_totals[1] + all_totals[2])
