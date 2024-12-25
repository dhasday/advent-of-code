from aoc.common import helpers
from aoc.common.day_solver import DaySolver


class Day25Solver(DaySolver):
    year = 2024
    day = 25

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        keys = list()
        locks = list()

        cur_item = [0, 0, 0, 0, 0]
        for idx in range(0, len(lines), 8):
            for i in range(idx + 1, idx + 6):
                for x, val in enumerate(lines[i]):
                    if val == '#':
                        cur_item[x] += 1
            if lines[idx] == '.....':
                keys.append(cur_item)
            else:
                locks.append(cur_item)
            cur_item = [0, 0, 0, 0, 0]

        count = 0
        for key in keys:
            for lock in locks:
                is_valid = True
                for i in range(5):
                    if key[i] + lock[i] > 5:
                        is_valid = False
                        break
                if is_valid:
                    count += 1
        return count, 'ALL DONE!'
