from aoc.common.day_solver import DaySolver


ROCK = '#'
ASH = '.'


class Day13Solver(DaySolver):
    year = 2023
    day = 13

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        patterns = []

        pattern = []
        for line in lines:
            if line == '':
                patterns.append(pattern)
                pattern = []
            else:
                pattern.append(line)
        if pattern:
            patterns.append(pattern)

        ans_one = 0
        ans_two = 0
        for pattern in patterns:
            cols_left, rows_above = self._get_reflection(pattern)
            ans_one += self._score_reflection(cols_left, rows_above)

            for row, col in self._get_all_positions(pattern):
                smudged = self._apply_smudge(pattern, row, col)
                new_cols_left, new_rows_above = self._get_reflection(smudged, cols_left, rows_above)
                if new_cols_left or new_rows_above:
                    ans_two += self._score_reflection(new_cols_left, new_rows_above)
                    break

        return ans_one, ans_two

    def _get_reflection(self, pattern, prev_cols_left=None, prev_rows_above=None):
        cols_left = self.get_reflect_vertical(pattern, prev_cols_left)
        if cols_left is not None:
            return cols_left, None

        rotated = self._rotate_pattern(pattern)
        rows_above = self.get_reflect_vertical(rotated, prev_rows_above)
        return None, rows_above

    def get_reflect_vertical(self, pattern, prev_cols_left):
        line_length = len(pattern[0])

        for column in range(1, line_length):
            if column == prev_cols_left:
                continue

            if self._all_match(pattern, column):
                return column

        return None

    def _all_match(self, pattern, column):
        lower_bound = 0
        upper_bound = len(pattern[0])
        upper_size = upper_bound - column

        if column > upper_size:
            lower_bound = column - upper_size
        elif column < upper_size:
            upper_bound = column + column

        for line in pattern:
            lower = line[lower_bound:column]
            upper = line[column:upper_bound][::-1]

            if lower != upper:
                return False

        return True

    def _rotate_pattern(self, pattern):
        # Reflect around x = y so we can reuse the column reflection logic
        rotated = [''] * len(pattern[0])

        for line in pattern:
            for idx, char in enumerate(line):
                rotated[idx] += char

        return rotated

    def _score_reflection(self, cols_left, rows_above):
        if cols_left:
            return cols_left
        if rows_above:
            return rows_above * 100
        return 0

    def _get_all_positions(self, pattern):
        for row in range(len(pattern)):
            for col in range(len(pattern[0])):
                yield row, col

    def _apply_smudge(self, pattern, row, col):
        smudge = ASH if pattern[row][col] == ROCK else ROCK

        smudged = pattern[:row]
        smudged.append(pattern[row][:col] + smudge + pattern[row][col + 1:])
        smudged.extend(pattern[row + 1:])

        return smudged
