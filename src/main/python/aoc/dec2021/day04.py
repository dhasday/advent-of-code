from aoc.common.day_solver import DaySolver
from aoc.common.helpers import ALL_NUMBERS_REGEX


SIZE = 5


class Day04Solver(DaySolver):
    year = 2021
    day = 4

    def solve_puzzles(self):
        called_numbers, all_boards = self._load_input()

        min_nums, min_score = self._calculate_board_win_value(called_numbers, all_boards[0])
        max_nums, max_score = min_nums, min_score

        for board in all_boards[1:]:
            win_nums, new_score = self._calculate_board_win_value(called_numbers, board)

            if win_nums is None:
                continue

            if win_nums < min_nums:
                min_nums = win_nums
                min_score = new_score
            if win_nums > max_nums:
                max_nums = win_nums
                max_score = new_score

        return min_score, max_score

    def _load_input(self):
        lines = self.load_all_input_lines()

        called_numbers = [int(i) for i in lines[0].split(',')]

        all_boards = []
        cur_board = []
        for line in lines[2:]:
            if not line:
                all_boards.append(cur_board)
                cur_board = []
            else:
                values = [int(v) for v in ALL_NUMBERS_REGEX.findall(line)]
                cur_board.extend(values)
        if cur_board:
            all_boards.append(cur_board)

        return called_numbers, all_boards

    def _calculate_board_win_value(self, called_numbers, board):
        total = sum(board)
        nums_called = 0
        num_index = {n: i for i, n in enumerate(board)}
        rows_called = [0] * SIZE
        cols_called = [0] * SIZE
        for num in called_numbers:
            nums_called += 1
            loc = num_index.get(num)
            if loc is not None:
                total -= num

                row = loc // SIZE
                rows_called[row] += 1

                col = loc % SIZE
                cols_called[col] += 1

                if rows_called[row] == SIZE or cols_called[col] == SIZE:
                    return nums_called, total * num

        return None, None
