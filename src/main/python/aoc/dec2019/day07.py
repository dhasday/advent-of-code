from aoc.common.day_solver import DaySolver
from aoc.dec2019.common.intcode_processor import IntcodeProcessor


class Day07Solver(DaySolver):
    year = 2019
    day = 7

    def solve_puzzle_one(self):
        line = self.load_only_input_line()

        options = self._generate_phase_options({0, 1, 2, 3, 4})
        max_output = None
        for (a, b, c, d, e) in options:
            processor_a, output_a = self._run_initial_execution(line, a, 0)
            processor_b, output_b = self._run_initial_execution(line, b, output_a)
            processor_c, output_c = self._run_initial_execution(line, c, output_b)
            processor_d, output_d = self._run_initial_execution(line, d, output_c)
            processor_e, output_e = self._run_initial_execution(line, e, output_d)

            if max_output is None or output_e > max_output:
                max_output = output_e

        return max_output

    def solve_puzzle_two(self):
        line = self.load_only_input_line()

        max_output = None

        options = self._generate_phase_options({5, 6, 7, 8, 9})
        for (a, b, c, d, e) in options:
            processor_a, output_a = self._run_initial_execution(line, a, 0)
            processor_b, output_b = self._run_initial_execution(line, b, output_a)
            processor_c, output_c = self._run_initial_execution(line, c, output_b)
            processor_d, output_d = self._run_initial_execution(line, d, output_c)
            processor_e, output_e = self._run_initial_execution(line, e, output_d)

            while processor_e.last_opcode != 99:
                output_a = self._run_until_output(processor_a, output_e)
                output_b = self._run_until_output(processor_b, output_a)
                output_c = self._run_until_output(processor_c, output_b)
                output_d = self._run_until_output(processor_d, output_c)
                output_e = self._run_until_output(processor_e, output_d)

            if max_output is None or output_e > max_output:
                max_output = output_e

        return max_output

    def _generate_phase_options(self, options):
        all_options = []

        for opt in options:
            if len(options) == 1:
                all_options.append([opt])
            else:
                sub_options = self._generate_phase_options(options.difference([opt]))
                for sub_opt in sub_options:
                    all_options.append([opt] + sub_opt)

        return all_options

    def _run_initial_execution(self, line, seed, input_value):
        processor = IntcodeProcessor(line, seed)
        processor.stop_after_instruction(3)
        processor.input_value = input_value
        processor.stop_after_instruction(4)
        return processor, processor.last_output

    def _run_until_output(self, processor, next_input):
        processor.input_value = next_input
        processor.stop_after_instruction(4)
        return processor.last_output
