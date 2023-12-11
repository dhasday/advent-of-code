from aoc.common.day_solver import DaySolver


class Day11Solver(DaySolver):
    year = 2023
    day = 11

    def solve_puzzle_one(self):
        lines = self.load_all_input_lines()

        return self._solve_with_expansions(lines, 1)

    def solve_puzzle_two(self):
        lines = self.load_all_input_lines()

        return self._solve_with_expansions(lines, 1_000_000)

    def _solve_with_expansions(self, lines, size):
        offset = max(size - 1, 1)

        expanded_cols = []
        empty_cols = []
        for col in range(len(lines[0])):
            if all(line[col] == '.' for line in lines):
                empty_cols.append(col)
            expanded_cols.append(col + (len(empty_cols) * offset))

        galaxy_locations = []
        empty_row_offset = 0
        for row, line in enumerate(lines):
            found_galaxy = False
            for col, val in enumerate(line):
                if val == '#':
                    found_galaxy = True
                    galaxy_locations.append((row + empty_row_offset, expanded_cols[col]))
            if not found_galaxy:
                empty_row_offset += offset

        total_distances = 0
        for idx, g1 in enumerate(galaxy_locations):
            for g2 in galaxy_locations[idx + 1:]:
                # Manhattan distance!
                total_distances += abs(g1[0] - g2[0]) + abs(g1[1] - g2[1])

        return total_distances
