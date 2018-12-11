from common.day_solver import DaySolver

INPUT = 1309


class Day11Solver(DaySolver):
    year = 2018
    day = 11

    memo = dict()

    def solve_puzzles(self):
        serial = INPUT
        grid_size = 300
        grid = [[self._calculate_power_level(x, y, serial) for y in range(grid_size)] for x in range(grid_size)]

        ans_one = self._max_three_by_three(grid)
        ans_two = self._max_any_size(grid, 20)

        return ans_one, ans_two

    def _calculate_power_level(self, x, y, serial):
        rack_id = (x + 1) + 10

        power_level = rack_id * (y + 1)
        power_level += serial
        power_level *= rack_id
        power_level = power_level // 100 % 10

        return power_level - 5

    def _max_three_by_three(self, grid):
        max_power = None
        max_pos = None

        for x in range(len(grid) - 3 + 1):
            for y in range(len(grid) - 3 + 1):
                power = self._get_total_power(grid, 3, x, y)

                if max_power is None or power > max_power:
                    max_power = power
                    max_pos = x + 1, y + 1

        return '{},{}'.format(max_pos[0], max_pos[1])

    def _max_any_size(self, grid, assumed_max_size=20):
        max_power = None
        max_pos = None
        max_size = None
        min_size_for_cur_max = 1

        for x in range(300):
            for y in range(300):
                if x + min_size_for_cur_max > 300 or y + min_size_for_cur_max > 300:
                    continue
                local_max = self._get_total_power(grid, min_size_for_cur_max, x, y)
                local_size = min_size_for_cur_max

                sum = local_max
                for s in range(min_size_for_cur_max, min(assumed_max_size, 300 - x, 300 - y)):
                    for i in range(x, x + s):
                        sum += grid[i][y + s]

                    for j in range(y, y + s):
                        sum += grid[x + s][j]

                    sum += grid[x + s][y + s]

                    if local_max is None or sum > local_max:
                        local_max = sum
                        local_size = s + 1

                if max_power is None or local_max > max_power:
                    max_power = local_max
                    max_size = local_size
                    max_pos = x + 1, y + 1
                    min_size_for_cur_max = (max_power / 4)

        return '{},{},{}'.format(max_pos[0], max_pos[1], max_size)

    def _get_total_power(self, grid, size, x, y):
        power = 0

        for i in range(size):
            for j in range(size):
                pos_x = x + i
                pos_y = y + j
                power += grid[pos_x][pos_y]

        return power
