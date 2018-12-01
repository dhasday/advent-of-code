from day_solver import DaySolver

INPUT_FILE = '../../resources/dec2018/1-input'
SEQUENCE_START_VALUE = 0


class Day01Solver(DaySolver):
    year = 2018
    day = 1

    def solve_puzzle_one(self):
        sequence = self._load_sequence()

        freq = SEQUENCE_START_VALUE
        for value in sequence:
            freq += value

        return freq

    def solve_puzzle_two(self):
        sequence = self._load_sequence()

        freq = SEQUENCE_START_VALUE
        seen_values = set()
        while True:
            for value in sequence:
                seen_values.add(freq)
                freq += value
                if freq in seen_values:
                    return freq

    def _load_sequence(self):
        sequence = []

        with open(INPUT_FILE) as f:
            for line in f:
                sequence.append(int(line))

        return sequence
