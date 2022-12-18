from aoc.common import helpers
from aoc.common.day_solver import DaySolver


class Day18Solver(DaySolver):
    year = 2022
    day = 18

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        cubes = set()
        mins = maxs = 0, 0, 0
        for line in lines:
            pos = eval(f'({line})')
            cubes.add(pos)
            mins = min(mins[0], pos[0]), min(mins[1], pos[1]), min(mins[2], pos[2])
            maxs = max(maxs[0], pos[0]), max(maxs[1], pos[1]), max(maxs[2], pos[2])

        water = self._find_all_water(mins, maxs, cubes)

        p1_total = 0
        p2_total = 0
        for cube in cubes:
            for deltas in helpers.STANDARD_DIRECTIONS_3D_MANHATTAN:
                cur_pos = helpers.apply_deltas(cube, deltas)

                if cur_pos not in cubes:
                    p1_total += 1
                    if cur_pos in water:
                        p2_total += 1
        return p1_total, p2_total

    def _find_all_water(self, min_values, max_values, cubes):
        # Add a boundary of 1 in all directions to surround all points
        min_values = min_values[0] - 1, min_values[1] - 1, min_values[2] - 1
        max_values = max_values[0] + 1, max_values[1] + 1, max_values[2] + 1

        water = set()
        open_set = set()
        closed_set = set()

        # Start in one corner and do a BFS
        open_set.add(min_values)
        while open_set:
            cur_loc = open_set.pop()
            closed_set.add(cur_loc)

            if min_values[0] > cur_loc[0] or cur_loc[0] > max_values[0] \
                    or min_values[1] > cur_loc[1] or cur_loc[1] > max_values[1] \
                    or min_values[2] > cur_loc[2] or cur_loc[2] > max_values[2]:
                continue

            if cur_loc in cubes:
                continue

            water.add(cur_loc)

            for delta in helpers.STANDARD_DIRECTIONS_3D_MANHATTAN:
                next_loc = cur_loc[0] + delta[0], cur_loc[1] + delta[1], cur_loc[2] + delta[2]
                if next_loc not in closed_set:
                    open_set.add(next_loc)
        return water
