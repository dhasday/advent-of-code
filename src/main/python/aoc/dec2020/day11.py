from aoc.common.day_solver import DaySolver

SEAT_EMPTY = 'L'
SEAT_OCCUPIED = '#'
SEAT_NONE = '.'

OFFSETS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]


class Day11Solver(DaySolver):
    year = 2020
    day = 11

    def solve_puzzle_one(self):
        seats = self.load_all_input_lines()

        num_rows = len(seats)
        num_cols = len(seats[0])

        while True:
            next_seats = []

            for y in range(num_rows):
                cur_row = ''
                for x in range(num_cols):
                    cur_value = seats[y][x]
                    if cur_value == SEAT_NONE:
                        cur_row += SEAT_NONE
                        continue

                    num_neighbors = self._num_neighbors(seats, num_rows, num_cols, x, y)
                    if cur_value == SEAT_EMPTY and num_neighbors == 0:
                        cur_row += SEAT_OCCUPIED
                    elif cur_value == SEAT_OCCUPIED and num_neighbors >= 4:
                        cur_row += SEAT_EMPTY
                    else:
                        cur_row += cur_value
                next_seats.append(cur_row)

            if next_seats == seats:
                break
            seats = next_seats

        count = 0
        for i in ''.join(seats):
            if i == SEAT_OCCUPIED:
                count += 1
        return count

    def solve_puzzle_two(self):
        seats = self.load_all_input_lines()

        num_rows = len(seats)
        num_cols = len(seats[0])

        while True:
            next_seats = []

            for y in range(num_rows):
                cur_row = ''
                for x in range(num_cols):
                    cur_value = seats[y][x]
                    if cur_value == SEAT_NONE:
                        cur_row += SEAT_NONE
                        continue

                    num_visible = self._num_visible(seats, num_rows, num_cols, x, y)
                    if cur_value == SEAT_EMPTY and num_visible == 0:
                        cur_row += SEAT_OCCUPIED
                    elif cur_value == SEAT_OCCUPIED and num_visible >= 5:
                        cur_row += SEAT_EMPTY
                    else:
                        cur_row += cur_value
                next_seats.append(cur_row)

            if next_seats == seats:
                break
            seats = next_seats

        count = 0
        for i in ''.join(seats):
            if i == SEAT_OCCUPIED:
                count += 1
        return count

    def _num_neighbors(self, seats, num_rows, num_cols, x, y):
        num_neighbors = 0

        for offset_x in range(-1, 2):
            pass

        for offset_x, offset_y in OFFSETS:
            neighbor_x = offset_x + x
            neighbor_y = offset_y + y
            if 0 <= neighbor_x < num_cols \
                    and 0 <= neighbor_y < num_rows \
                    and seats[neighbor_y][neighbor_x] == SEAT_OCCUPIED:
                num_neighbors += 1

        return num_neighbors

    def _num_visible(self, seats, num_rows, num_cols, x, y):
        num_visible = 0

        for offset_x, offset_y in OFFSETS:
            first_visible = self._first_visible_in_direction(seats, num_rows, num_cols, x, y, offset_x, offset_y)
            if first_visible == SEAT_OCCUPIED:
                num_visible += 1

        return num_visible

    def _first_visible_in_direction(self, seats, num_rows, num_cols, start_x, start_y, offset_x, offset_y):
        cur_x = start_x
        cur_y = start_y

        while True:
            cur_x += offset_x
            cur_y += offset_y

            if cur_x < 0 or cur_x >= num_cols:
                return '.'
            if cur_y < 0 or cur_y >= num_rows:
                return '.'

            cur_seat = seats[cur_y][cur_x]
            if cur_seat in [SEAT_EMPTY, SEAT_OCCUPIED]:
                return cur_seat
