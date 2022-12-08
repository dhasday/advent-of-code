from aoc.common.day_solver import DaySolver


class Day08Solver(DaySolver):
    year = 2022
    day = 8

    def solve_puzzles(self):
        grid = self.load_all_input_lines()
        num_rows = len(grid)
        num_cols = len(grid[0])

        edge_visible = 0
        max_score = 0
        for i in range(num_rows):
            for j in range(num_cols):
                cur_score, cur_visible = self._process_tree(grid, num_rows, num_cols, i, j)
                max_score = max(max_score, cur_score)
                if cur_visible:
                    edge_visible += 1
        return edge_visible, max_score

    def _process_tree(self, grid, num_rows, num_cols, x, y):
        max_value = int(grid[x][y])

        score = 1
        can_see_edge = False

        for dr, dc in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            cur_count = 0
            cur_edge = True
            cur_row = x + dr
            cur_col = y + dc
            while 0 <= cur_row < num_rows and 0 <= cur_col < num_cols:
                cur_value = int(grid[cur_row][cur_col])
                cur_count += 1
                cur_row += dr
                cur_col += dc

                if cur_value >= max_value:
                    cur_edge = False
                    break

            score *= cur_count
            can_see_edge |= cur_edge

        return score, can_see_edge
