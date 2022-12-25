from collections import deque

from aoc.common.day_solver import DaySolver


class Day20Solver(DaySolver):
    year = 2022
    day = 20

    def solve_puzzle_one(self):
        return self._decrypt(1, 1)

    def solve_puzzle_two(self):
        decryption_key = 811589153
        iterations = 10
        return self._decrypt(decryption_key, iterations)

    def _decrypt(self, decryption_key, iterations):
        lines = self.load_all_input_lines()

        values = [int(line) * decryption_key for line in lines]
        indices = deque(range(len(values)))

        for _ in range(iterations):
            indices = self._mix_values(values, indices)
        return self._get_coordinates(values, indices)

    def _mix_values(self, values, indices):
        for i, value in enumerate(values):
            cur_pos = indices.index(i)
            indices.rotate(-cur_pos)
            indices.popleft()
            indices.rotate(-value)
            indices.appendleft(i)
        return indices

    def _get_coordinates(self, values, indices):
        zero_index = indices.index(values.index(0))
        return sum(values[indices[(zero_index + v) % len(values)]] for v in [1000, 2000, 3000])
