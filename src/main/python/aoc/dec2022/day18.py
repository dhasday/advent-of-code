from aoc.common import helpers
from aoc.common.day_solver import DaySolver


class Day18Solver(DaySolver):
    year = 2022
    day = 18

    def solve_puzzle_one(self):
        lines = self.load_all_input_lines()

        cubes = set()

        for line in lines:
            pos = eval(f'({line})')
            cubes.add(pos)

        total = 0
        for cube in cubes:
            for adj in helpers.STANDARD_DIRECTIONS_3D_MANHATTAN:
                cur_pos = (cube[0] + adj[0], cube[1] + adj[1], cube[2] + adj[2])
                if cur_pos in cubes:
                    continue
                total += 1
        return total

    def solve_puzzle_two(self):
        lines = self.load_all_input_lines()

        cubes = set()
        mins = maxs = 0, 0, 0
        for line in lines:
            pos = eval(f'({line})')
            cubes.add(pos)
            mins = min(mins[0], pos[0]), min(mins[1], pos[1]), min(mins[2], pos[2])
            maxs = max(maxs[0], pos[0]), max(maxs[1], pos[1]), max(maxs[2], pos[2])

        # Add a boundary of 1 in all directions to surround all points
        mins = mins[0] - 1, mins[1] - 1, mins[2] - 1
        maxs = maxs[0] + 1, maxs[1] + 1, maxs[2] + 1

        water = set()
        open_set = set()
        open_set.add(mins)
        closed_set = set()
        while open_set:
            cur_loc = open_set.pop()
            closed_set.add(cur_loc)

            if cur_loc in cubes:
                continue

            water.add(cur_loc)

            cx, cy, cz = cur_loc
            for dx, dy, dz in helpers.STANDARD_DIRECTIONS_3D_MANHATTAN:
                next_loc = cx + dx, cy + dy, cz + dz
                if next_loc not in closed_set \
                        and mins[0] <= next_loc[0] <= maxs[0] \
                        and mins[1] <= next_loc[1] <= maxs[1] \
                        and mins[2] <= next_loc[2] <= maxs[2]:
                    open_set.add(next_loc)

        count = 0
        for cube in cubes:
            cx, cy, cz = cube
            for dx, dy, dz in helpers.STANDARD_DIRECTIONS_3D_MANHATTAN:
                next_loc = cx + dx, cy + dy, cz + dz
                if next_loc in water:
                    count += 1
        return count
