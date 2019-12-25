from collections import deque

from aoc.common.day_solver import DaySolver
from aoc.common.helpers import ALL_NUMBERS_REGEX
from aoc.dec2019.common.intcode_processor import IntcodeProcessor


class Day25Solver(DaySolver):
    year = 2019
    day = 25

    input_queue = deque()

    def solve_puzzle_one(self):
        line = self.load_only_input_line()

        processor = IntcodeProcessor(program_str=line, input_func=self.input_queue.popleft)

        self._load_instructions()
        output = self._run_until_end(processor, debug=False)

        return ALL_NUMBERS_REGEX.findall(output)[0]

    def solve_puzzle_two(self):
        return 'ALL DONE!'

    def _load_instructions(self):
        instructions = self.load_all_input_lines(filename='25-p1')
        for i in instructions:
            self.input_queue.extend([ord(c) for c in i])
            self.input_queue.append(ord('\n'))

    def _run_until_end(self, processor, debug=False):
        line = ''
        output = ''
        while True:
            out = processor.get_next_output()
            if processor.last_opcode == 99:
                break
            last_char = chr(out)
            output += last_char

            if debug:
                if last_char == '\n':
                    print(line)
                    line = ''
                else:
                    line += last_char
        return output


if __name__ == '__main__':
    Day25Solver().print_results()
