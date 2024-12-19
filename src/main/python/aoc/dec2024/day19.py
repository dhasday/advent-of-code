from aoc.common.day_solver import DaySolver


class Day19Solver(DaySolver):
    year = 2024
    day = 19

    towel_options = None
    cached_counts = None

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        self.cached_counts = {'': 1}
        self.towel_options = lines[0].split(', ')
        desired_designs = lines[2:]

        possible_count = 0
        total_count = 0
        for design in desired_designs:
            count = self._design_counts(design)
            if count:
                possible_count += 1
                total_count += count

        return possible_count, total_count

    def _design_counts(self, design):
        if design in self.cached_counts:
            return self.cached_counts[design]

        count = 0
        for option in self.towel_options:
            if design.startswith(option):
                count += self._design_counts(design[len(option):])

        self.cached_counts[design] = count
        return count
