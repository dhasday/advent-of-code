from aoc.common.day_solver import DaySolver


class Day01Solver(DaySolver):
    year = 2020
    day = 1

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        values = [int(v) for v in lines]
        num = len(values)

        ans_1 = None
        ans_2 = None
        for x in range(num):
            val_1 = values[x]
            if ans_1 and ans_2:
                break
            for y in range(num):
                val_2 = values[y]
                if ans_1 is None and val_1 + val_2 == 2020:
                    ans_1 = val_1 * val_2
                    break
                for z in range(num):
                    val_3 = values[z]
                    if ans_2 is None and val_1 + val_2 + val_3 == 2020:
                        ans_2 = val_1 * val_2 * val_3
                        break
        return ans_1, ans_2
