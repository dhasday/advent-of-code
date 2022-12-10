from aoc.common.day_solver import DaySolver
from aoc.common.helpers import split_layers
from aoc.common.letter_reader import read_output


class Day10Solver(DaySolver):
    year = 2022
    day = 10

    def solve_puzzles(self):
        def should_light():
            return abs(cur_value - (cur_cycle % 40)) <= 1

        lines = self.load_all_input_lines()

        cur_value = 1
        ptr = 0
        cur_cycle = 0

        total_readings = 0
        next_reading = 20
        output = ''
        while cur_cycle < 240:
            cur_line = lines[ptr]
            ptr += 1

            ins = cur_line.split(' ')
            if ins[0] == 'noop':
                output += '0' if should_light() else ' '
                cur_cycle += 1
                new_value = cur_value
            elif ins[0] == 'addx':
                output += '0' if should_light() else ' '
                cur_cycle += 1
                output += '0' if should_light() else ' '
                cur_cycle += 1
                new_value = cur_value + int(ins[1])
            else:
                raise Exception(f'Unsupported instruction: {ins[0]}')

            if cur_cycle >= next_reading:
                total_readings += (next_reading * cur_value)
                next_reading += 40
            cur_value = new_value

        return total_readings, read_output(split_layers(output, 40))
