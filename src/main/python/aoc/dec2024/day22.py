from collections import deque, defaultdict

from aoc.common.day_solver import DaySolver

MODULO_DIVISOR = 16777216


class Day22Solver(DaySolver):
    year = 2024
    day = 22

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        total_p1 = 0
        all_deltas = defaultdict(int)
        for line in lines:
            seen_deltas = set()
            secret_num = int(line)
            prev_bananas = secret_num % 10

            cur_deltas = deque()

            for _ in range(3):
                secret_num = self._get_next_secret_number(secret_num)
                cur_bananas = secret_num % 10
                cur_deltas.append(cur_bananas - prev_bananas)
                prev_bananas = cur_bananas

            for i in range(1997):
                secret_num = self._get_next_secret_number(secret_num)
                cur_bananas = secret_num % 10
                cur_deltas.append(cur_bananas - prev_bananas)
                deltas = tuple(cur_deltas)
                if deltas not in seen_deltas:
                    all_deltas[deltas] += cur_bananas
                    seen_deltas.add(deltas)
                prev_bananas = cur_bananas
                cur_deltas.popleft()
            total_p1 += secret_num

        return total_p1, max(all_deltas.values())

    def _get_next_secret_number(self, secret_num):
        secret_num = ((secret_num * 64) ^ secret_num) % MODULO_DIVISOR
        secret_num = ((secret_num // 32) ^ secret_num) % MODULO_DIVISOR
        secret_num = ((secret_num * 2048) ^ secret_num) % MODULO_DIVISOR
        return secret_num
