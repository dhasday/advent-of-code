from aoc.common import helpers
from aoc.common.day_solver import DaySolver


class Day04Solver(DaySolver):
    year = 2025
    day = 4

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        max_y = len(lines)
        max_x = len(lines[0])
        rolls = dict()
        for y, line in enumerate(lines):
            for x, val in enumerate(line):
                if val == '@':
                    neighbors = 0
                    for dx, dy in helpers.STANDARD_DIRECTIONAL_OFFSETS:
                        x1 = x + dx
                        y1 = y + dy
                        if 0 <= x1 < max_x and 0 <= y1 < max_y and lines[y1][x1] == '@':
                            neighbors += 1
                    rolls[x, y] = neighbors

        to_remove = set(roll for roll, neighbors in rolls.items() if neighbors < 4)
        initially_accessible = len(to_remove)
        initial_count = len(rolls)

        while to_remove:
            roll = to_remove.pop()
            del rolls[roll]

            for dx, dy in helpers.STANDARD_DIRECTIONAL_OFFSETS:
                neighbor = roll[0] + dx, roll[1] + dy
                if neighbor in rolls and neighbor not in to_remove:
                    rolls[neighbor] -= 1
                    if rolls[neighbor] < 4:
                        to_remove.add(neighbor)

        total_removed = initial_count - len(rolls)
        return initially_accessible, total_removed
