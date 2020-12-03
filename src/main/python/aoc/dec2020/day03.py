from aoc.common.day_solver import DaySolver


class Day03Solver(DaySolver):
    year = 2020
    day = 3

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        height = len(lines)
        width = len(lines[0])

        trees = set()
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == '#':
                    trees.add((x, y))

        n_1 = self._get_num_trees_hit_for_slope(height, width, trees, 1, 1)
        n_2 = self._get_num_trees_hit_for_slope(height, width, trees, 3, 1)
        n_3 = self._get_num_trees_hit_for_slope(height, width, trees, 5, 1)
        n_4 = self._get_num_trees_hit_for_slope(height, width, trees, 7, 1)
        n_5 = self._get_num_trees_hit_for_slope(height, width, trees, 1, 2)

        ans_1 = n_2
        ans_2 = n_1 * n_2 * n_3 * n_4 * n_5
        return ans_1, ans_2

    def _get_num_trees_hit_for_slope(self, height, width, trees, dx, dy):
        trees_hit = 0
        cur_x = cur_y = 0
        while cur_y < height:
            if (cur_x % width, cur_y) in trees:
                trees_hit += 1
            cur_x += dx
            cur_y += dy

        return trees_hit
