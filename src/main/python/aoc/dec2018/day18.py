from collections import defaultdict, Counter

from aoc.common.day_solver import DaySolver


OPEN_GROUND = '.'
TREES = '|'
LUMBERYARD = '#'

MEMO = defaultdict(lambda: {})

NEIGHBOR_OFFSETS = []
for i in range(-1, 2):
    for j in range(-1, 2):
        if i != 0 or j != 0:
            NEIGHBOR_OFFSETS.append((i, j))


class Day18Solver(DaySolver):
    year = 2018
    day = 18

    def solve_puzzle_one(self):
        area = self._load_all_input_lines()
        size = len(area)

        for _ in range(10):
            area = self._update_area(area, size)

        area_counts = Counter(''.join(area))
        return area_counts[LUMBERYARD] * area_counts[TREES]

    def solve_puzzle_two(self):
        total_iters = 1000000000
        area = self._load_all_input_lines()
        size = len(area)

        loop_states, loop_start = self._find_loop(area, size)
        loop_offset = (total_iters - loop_start) % len(loop_states)

        area_counts = Counter(loop_states[loop_offset])
        return area_counts[LUMBERYARD] * area_counts[TREES]

    def _update_area(self, cur_area, size):
        next_area = [''] * size

        for y in range(size):
            for x in range(size):
                cur_val = cur_area[x][y]
                neighbors = self._get_neighbors(cur_area, size, x, y)

                neighbors_memo = MEMO.get(neighbors)
                if not neighbors_memo or cur_val not in neighbors_memo:
                    counts = Counter(neighbors)

                    next_val = cur_val
                    if cur_val == OPEN_GROUND and counts.get(TREES) >= 3:
                        next_val = TREES
                    elif cur_val == TREES and counts.get(LUMBERYARD) >= 3:
                        next_val = LUMBERYARD
                    elif cur_val == LUMBERYARD and (counts.get(LUMBERYARD) < 1 or counts.get(TREES) < 1):
                        next_val = OPEN_GROUND
                    MEMO[neighbors][cur_val] = next_val
                    neighbors_memo = MEMO[neighbors]

                next_area[x] += neighbors_memo[cur_val]

        return next_area

    def _get_neighbors(self, cur_area, size, x, y):
        neighbors = ''

        for offset in NEIGHBOR_OFFSETS:
            col = offset[0] + x
            row = offset[1] + y

            if 0 <= col < size and 0 <= row < size:
                neighbors += cur_area[col][row]

        return neighbors

    def _find_loop(self, area, size):
        seen_areas = list()
        str_area = None
        ctr = 0

        while ctr < 1000:
            area = self._update_area(area, size)
            ctr += 1

            str_area = ''.join(area)
            if str_area in seen_areas:
                break

            seen_areas.append(str_area)

        return seen_areas[seen_areas.index(str_area):], ctr
