from aoc.common.chinese_remainder import chinese_remainder
from aoc.common.day_solver import DaySolver


class Day13Solver(DaySolver):
    year = 2020
    day = 13

    def solve_puzzle_one(self):
        lines = self.load_all_input_lines()

        cur_timestamp = int(lines[0])

        min_bus = None
        min_time = None
        for line in lines[1].split(','):
            if line == 'x':
                continue

            bus = int(line)
            time_since_last_bus = cur_timestamp % bus
            next_bus = cur_timestamp + bus - time_since_last_bus

            if min_time is None or next_bus < min_time:
                min_bus = bus
                min_time = next_bus

        return min_bus * (min_time - cur_timestamp)

    def solve_puzzle_two(self):
        lines = self.load_all_input_lines()

        raw_buses = lines[1].split(',')
        divisors = []
        remainders = []
        for idx, raw_bus in enumerate(raw_buses):
            if raw_bus != 'x':
                divisors.append(int(raw_bus))
                remainders.append(-idx)

        return chinese_remainder(divisors, remainders)
