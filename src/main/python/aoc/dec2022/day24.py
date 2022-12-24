from aoc.common import helpers
from aoc.common.day_solver import DaySolver


DIRECTION_OFFSETS = {
    '<': (-1, 0),
    '>': (1, 0),
    '^': (0, -1),
    'v': (0, 1),
}


class Day24Solver(DaySolver):
    year = 2022
    day = 24

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        blizzards = set()
        for y, line in enumerate(lines[1:-1], start=1):
            for x, c in enumerate(line):
                if c in DIRECTION_OFFSETS:
                    blizzards.add(((x, y), DIRECTION_OFFSETS[c]))

        max_x = len(lines[0]) - 2
        max_y = len(lines) - 2
        start_pos = lines[0].index('.'), 0
        end_pos = lines[-1].index('.'), max_y + 1

        current_positions = set()
        current_positions.add(start_pos)

        blizzards, min_time_1 = self._find_path(blizzards, start_pos, end_pos, max_x, max_y)
        blizzards, min_time_2 = self._find_path(blizzards, end_pos, start_pos, max_x, max_y)
        blizzards, min_time_3 = self._find_path(blizzards, start_pos, end_pos, max_x, max_y)

        p1 = min_time_1
        # Need to add 2 to count the first min of trips 2 and 3
        p2 = min_time_1 + min_time_2 + min_time_3 + 2
        return p1, p2

    def _find_path(self, blizzards, start_pos, end_pos, max_x, max_y):
        current_positions = set()
        current_positions.add(start_pos)

        for minute in range(500):
            blizzard_locations = set(b[0] for b in blizzards)
            next_positions = set()
            for pos in current_positions:
                for offset in helpers.STANDARD_DIRECTIONS:
                    next_pos = helpers.apply_deltas(pos, offset)
                    if next_pos[0] < 1 or next_pos[0] > max_x or next_pos[1] < 1 or next_pos[1] > max_y:
                        if next_pos not in [start_pos, end_pos]:
                            continue
                    if next_pos not in blizzard_locations:
                        next_positions.add(next_pos)
                if pos not in blizzard_locations:
                    next_positions.add(pos)
            current_positions = next_positions
            blizzards = self._advance_blizzards(blizzards, max_x, max_y)
            if end_pos in next_positions:
                return blizzards, minute

        raise Exception('Trip is taking longer than expected, add some more time and maybe it\'ll work')

    def _advance_blizzards(self, current_blizzards, max_x, max_y):
        next_blizzards = set()
        for loc, offset in current_blizzards:
            next_loc = helpers.apply_deltas(loc, offset)
            if next_loc[0] == 0:
                next_loc = max_x, next_loc[1]
            if next_loc[0] > max_x:
                next_loc = 1, next_loc[1]
            if next_loc[1] == 0:
                next_loc = next_loc[0], max_y
            if next_loc[1] > max_y:
                next_loc = next_loc[0], 1
            next_blizzards.add((next_loc, offset))

        return next_blizzards
