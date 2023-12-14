from aoc.common.day_solver import DaySolver

EMPTY = '.'
ROUND_ROCK = 'O'
SQUARE_ROCK = '#'


class Day14Solver(DaySolver):
    year = 2023
    day = 14

    def solve_puzzle_one(self):
        lines = self.load_all_input_lines()

        num_rows = len(lines)
        num_cols = len(lines[0])

        lines = self._roll_north(num_rows, num_cols, lines)

        return self._calculate_load_north(lines)

    def solve_puzzle_two(self):
        lines = self.load_all_input_lines()

        num_rows = len(lines)
        num_cols = len(lines[0])

        cur = None
        cur_lines = lines
        seen = []
        for _ in range(500):
            cur = ','.join(cur_lines)

            if cur in seen:
                break
            seen.append(cur)

            cur_lines = self._roll_north(num_rows, num_cols, cur_lines)
            cur_lines = self._roll_west(num_rows, num_cols, cur_lines)
            cur_lines = self._roll_south(num_rows, num_cols, cur_lines)
            cur_lines = self._roll_east(num_rows, num_cols, cur_lines)

        assert cur in seen

        loop_size = len(seen) - seen.index(cur)
        loop_start = len(seen) - loop_size
        offset = (1_000_000_000 - loop_start) % loop_size

        result = seen[loop_start + offset].split(',')

        return self._calculate_load_north(result)

    def _roll_north(self, num_rows, num_cols, lines):
        new_lines = ['.' * num_cols] * num_rows

        for col in range(num_cols):
            min_row = 0
            for row in range(num_rows):
                cur_val = lines[row][col]
                if cur_val == ROUND_ROCK:
                    new_lines[min_row] = new_lines[min_row][:col] + ROUND_ROCK + new_lines[min_row][col + 1:]
                    min_row += 1
                elif cur_val == SQUARE_ROCK:
                    new_lines[row] = new_lines[row][:col] + SQUARE_ROCK + new_lines[row][col + 1:]
                    min_row = row + 1

        return new_lines

    def _roll_west(self, num_rows, num_cols, lines):
        new_lines = []

        for row in range(num_rows):
            new_line = ''
            min_col = 0
            for col in range(num_cols):
                cur_val = lines[row][col]
                if cur_val == ROUND_ROCK:
                    new_line = new_line[:min_col] + ROUND_ROCK + new_line[min_col:]
                    min_col += 1
                elif cur_val == SQUARE_ROCK:
                    new_line += SQUARE_ROCK
                    min_col = col + 1
                else:
                    new_line += EMPTY
            new_lines.append(new_line)

        return new_lines

    def _roll_south(self, num_rows, num_cols, lines):
        new_lines = ['.' * num_cols] * num_rows

        for col in range(num_cols):
            max_row = num_rows - 1
            for row in range(num_rows - 1, -1, -1):
                cur_val = lines[row][col]
                if cur_val == ROUND_ROCK:
                    new_lines[max_row] = new_lines[max_row][:col] + ROUND_ROCK + new_lines[max_row][col + 1:]
                    max_row -= 1
                elif cur_val == SQUARE_ROCK:
                    new_lines[row] = new_lines[row][:col] + SQUARE_ROCK + new_lines[row][col + 1:]
                    max_row = row - 1

        return new_lines

    def _roll_east(self, num_rows, num_cols, lines):
        new_lines = []

        for row in range(num_rows):
            new_line = EMPTY * num_cols
            max_col = num_cols - 1
            for col in range(num_cols - 1, -1, -1):
                cur_val = lines[row][col]
                if cur_val == ROUND_ROCK:
                    new_line = new_line[:max_col] + ROUND_ROCK + new_line[max_col + 1:]
                    max_col -= 1
                elif cur_val == SQUARE_ROCK:
                    new_line = new_line[:col] + SQUARE_ROCK + new_line[col + 1:]
                    max_col = col - 1
            new_lines.append(new_line)

        return new_lines

    def _calculate_load_north(self, lines):
        total = 0
        num_rows = len(lines)
        for idx, line in enumerate(lines):
            for val in line:
                if val == ROUND_ROCK:
                    total += num_rows - idx
        return total
