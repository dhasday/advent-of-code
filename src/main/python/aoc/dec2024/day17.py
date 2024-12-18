from aoc.common import helpers
from aoc.common.day_solver import DaySolver
from aoc.dec2024.common.three_bit_computer import ThreeBitComputer


class Day17Solver(DaySolver):
    year = 2024
    day = 17

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        values = helpers.parse_all_numbers('\n'.join(lines))

        reg_a = values[0]
        reg_b = values[1]
        reg_c = values[2]
        instructions = values[3:]

        computer = ThreeBitComputer(reg_a, reg_b, reg_c, instructions)

        ans_one = ','.join(str(v) for v in computer.run_until_end())

        options = [0]
        for x in range(len(instructions), 0, -1):
            new_options = []
            target = instructions[x-1:]
            for option in options:
                next_option = 8 * option
                for new_option in range(next_option, next_option + 8):
                    if self._check_run_result(computer, new_option, target):
                        new_options.append(new_option)
            options = new_options
        return ans_one, min(options)

    def _check_run_result(self, computer, start_a, target_seq):
        computer.reset(reg_a=start_a)

        idx = 0
        while idx < len(target_seq):
            next_val = computer.run_until_output()
            if next_val != target_seq[idx]:
                return False
            idx += 1
        return True
