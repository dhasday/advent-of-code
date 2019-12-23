from collections import deque

from aoc.common.day_solver import DaySolver
from aoc.dec2019.common.intcode_processor import IntcodeProcessor


class Day21Solver(DaySolver):
    year = 2019
    day = 21

    class Springdroid(object):

        instructions = deque()

        def __init__(self, program_str):
            self.processor = IntcodeProcessor(program_str=program_str, input_func=self._input_func)

        def _input_func(self):
            if len(self.instructions):
                return self.instructions.popleft()
            else:
                return None

        def add_instruction(self, instruction):
            for c in instruction:
                self.instructions.append(ord(c))
            self.instructions.append(ord('\n'))

        def walk(self, debug=False):
            self.add_instruction('WALK')
            return self._execute(debug)

        def run(self, debug=False):
            self.add_instruction('RUN')
            return self._execute(debug)

        def _execute(self, debug):
            self.processor.reset()
            output = ''
            while True:
                out = self.processor.get_next_output()
                if self.processor.last_opcode != 99:
                    if out > 127:
                        if debug:
                            print(output)
                        output = out
                    else:
                        output += chr(out)
                else:
                    return output

    def solve_puzzle_one(self):
        line = self.load_only_input_line()

        program = self.Springdroid(program_str=line)

        # ( !A | !C ) & D
        program.add_instruction('NOT A J')
        program.add_instruction('NOT C T')
        program.add_instruction('OR T J')
        program.add_instruction('AND D J')

        output = program.walk()
        assert isinstance(output, int)
        return output

    def solve_puzzle_two(self):
        line = self.load_only_input_line()

        program = self.Springdroid(line)

        # !(A | B | C) & D & (E | H)
        program.add_instruction('OR A J')
        program.add_instruction('AND B J')
        program.add_instruction('AND C J')
        program.add_instruction('NOT J J')
        program.add_instruction('AND D J')
        program.add_instruction('OR E T')
        program.add_instruction('OR H T')
        program.add_instruction('AND T J')

        output = program.run()
        assert isinstance(output, int)
        return output
