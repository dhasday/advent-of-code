from aoc.common.day_solver import DaySolver

SEQUENCE_START_VALUE = 0


class Day02Solver(DaySolver):
    year = 2019
    day = 2

    def solve_puzzle_one(self):
        line = self._load_only_input_line()

        values = [int(v) for v in line.split(',')]
        values[1] = 12
        values[2] = 2

        return self._process_instructions(values)

    def solve_puzzle_two(self):
        line = self._load_only_input_line()

        values = [int(v) for v in line.split(',')]

        for i in range(0, 99):
            for j in range(0, 99):
                test_values = values.copy()
                test_values[1] = i
                test_values[2] = j

                result = self._process_instructions(test_values)

                if result == 19690720:
                    return (i * 100) + j

        return None

    def _process_instructions(self, values):
        index = 0

        while True:
            code = values[index]

            if code == 1:
                # Do addition
                next_pos = values[index + 3]
                values[next_pos] = values[values[index + 1]] + values[values[index + 2]]
            elif code == 2:
                # Do multiplication
                next_pos = values[index + 3]
                values[next_pos] = values[values[index + 1]] * values[values[index + 2]]
            elif code == 99:
                # End
                return values[0]
            else:
                raise Exception('You dun fucked up')

            index += 4
