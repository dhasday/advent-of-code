from aoc.common.day_solver import DaySolver
from aoc.common.helpers import STANDARD_DIRECTIONAL_OFFSETS

SEAT_EMPTY = 'L'
SEAT_OCCUPIED = '#'
SEAT_NONE = '.'


class Day11Solver(DaySolver):
    year = 2020
    day = 11

    def solve_puzzles(self):
        lines = self.load_all_input_lines()
        num_rows = len(lines)
        num_cols = len(lines[0])
        seats = dict()
        for y, line in enumerate(lines):
            for x, cur in enumerate(line):
                if cur in [SEAT_EMPTY, SEAT_OCCUPIED]:
                    seats[(x, y)] = cur == SEAT_OCCUPIED

        ans_one = self._solve_part_one(seats)
        ans_two = self._solve_part_two(seats, num_rows, num_cols)

        return ans_one, ans_two

    def _solve_part_one(self, seats):
        while True:
            next_seats = dict()
            changed = False

            for seat, value in seats.items():
                num_neighbors = self._num_neighbors(seats, seat)
                if value and num_neighbors >= 4:
                    next_seats[seat] = False
                    changed = True
                elif not value and num_neighbors == 0:
                    next_seats[seat] = True
                    changed = True
                else:
                    next_seats[seat] = value

            seats = next_seats
            if not changed:
                break

        return self._count_occupied(seats)

    def _solve_part_two(self, seats, num_rows, num_cols):
        while True:
            next_seats = dict()
            changed = False

            for seat, value in seats.items():
                num_visible = self._num_visible(seats, num_rows, num_cols, seat)
                if value and num_visible >= 5:
                    next_seats[seat] = False
                    changed = True
                elif not value and num_visible == 0:
                    next_seats[seat] = True
                    changed = True
                else:
                    next_seats[seat] = value

            seats = next_seats
            if not changed:
                break

        return self._count_occupied(seats)

    def _num_neighbors(self, seats, seat):
        count = 0
        x, y = seat
        for offset_x, offset_y in STANDARD_DIRECTIONAL_OFFSETS:
            value = seats.get((x + offset_x, y + offset_y), False)
            if value:
                count += 1
        return count

    def _num_visible(self, seats, num_rows, num_cols, seat):
        num_visible = 0

        for offset_x, offset_y in STANDARD_DIRECTIONAL_OFFSETS:
            first_visible = self._first_visible_in_direction(seats, num_rows, num_cols, seat, offset_x, offset_y)
            if first_visible:
                num_visible += 1

        return num_visible

    def _first_visible_in_direction(self, seats, num_rows, num_cols, seat, offset_x, offset_y):
        cur_x, cur_y = seat

        while True:
            cur_x += offset_x
            cur_y += offset_y

            if cur_x < 0 or cur_x >= num_cols:
                return False
            if cur_y < 0 or cur_y >= num_rows:
                return False

            cur_seat = cur_x, cur_y
            cur_value = seats.get(cur_seat, None)
            if cur_value is not None:
                return cur_value

    def _count_occupied(self, seats):
        return list(seats.values()).count(True)
