from collections import defaultdict

from aoc.common.day_solver import DaySolver


class Day05Solver(DaySolver):
    year = 2020
    day = 5

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        max_seat_id = 0
        remaining_seats = defaultdict(lambda: set(s for s in range(8)))
        for line in lines:
            row = self._follow_directions(line[:7], 128)
            seat = self._follow_directions(line[7:], 8)
            seat_id = (row * 8) + seat

            max_seat_id = max(seat_id, max_seat_id)
            remaining_seats[row].discard(seat)

        missing_seat = self._find_missing_seat(remaining_seats)

        return max_seat_id, missing_seat

    def _follow_directions(self, directions, quantity):
        min_row = 0
        max_row = quantity - 1
        rows_remaining = quantity

        for d in directions:
            rows_remaining //= 2

            if d in ['F', 'L']:  # Keep Front Half
                max_row -= rows_remaining
            else:  # Keep Back Half
                min_row += rows_remaining

        return min_row

    def _find_missing_seat(self, remaining_seats):
        for row, seats in remaining_seats.items():
            if len(seats) == 1:
                seat = seats.pop()
                return row * 8 + seat
        return None
