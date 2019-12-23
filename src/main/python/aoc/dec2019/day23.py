from collections import deque

from aoc.common.day_solver import DaySolver
from aoc.dec2019.common.intcode_processor import IntcodeProcessor

NUM_NODES = 50


class Day23Solver(DaySolver):
    year = 2019
    day = 23

    def solve_puzzles(self):
        processors, queued_values = self._init_processors()

        first_nat_y, first_repeat_nat_y = self._run_processors(processors, queued_values)

        return first_nat_y, first_repeat_nat_y

    def _init_processors(self):
        def input_func(idx):
            buffered = queued_values[idx]
            return lambda: buffered.popleft() if len(buffered) else -1

        line = self.load_only_input_line()

        processors = []
        queued_values = [deque() for _ in range(NUM_NODES)]
        for i in range(NUM_NODES):
            processor = IntcodeProcessor(line, input_value=i)
            processor.execute_current_step()
            processor.input_func = input_func(i)
            processors.append(processor)

        return processors, queued_values

    def _run_processors(self, processors, queued_values):
        output_values = [[] for _ in range(NUM_NODES)]
        idling = [False] * NUM_NODES
        first_nat_y = None
        nat_output = None
        prev_output = None
        while True:
            for i in range(NUM_NODES):
                p = processors[i]

                if p.get_next_opcode() == 3:
                    if len(queued_values[i]) == 0:
                        idling[i] = True
                    else:
                        idling[i] = False

                p.execute_current_step()

                if p.last_opcode == 4:
                    out = output_values[i]
                    if len(out) < 2:
                        out.append(p.last_output)
                    else:
                        addr = out[0]
                        x = out[1]
                        y = p.last_output

                        if 0 <= addr <= 49:
                            queued_values[addr].append(x)
                            queued_values[addr].append(y)
                        elif addr == 255:
                            nat_output = x, y
                            if not first_nat_y:
                                first_nat_y = y

                        output_values[i] = []

            if nat_output is not None and all(idling):
                if prev_output == nat_output:
                    return first_nat_y, nat_output[1]

                queued_values[0].append(nat_output[0])
                queued_values[0].append(nat_output[1])
                prev_output = nat_output
                idling = [False] * NUM_NODES


if __name__ == '__main__':
    Day23Solver().print_results()
