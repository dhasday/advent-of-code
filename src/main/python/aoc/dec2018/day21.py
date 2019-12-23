from aoc.common.day_solver import DaySolver
from aoc.dec2018.common.chrono_assembly import ChronoProcessor

INSTRUCION_POINTER = 2
R0_COMPARE_INSTRUCTION = 28


class Day21Solver(DaySolver):
    year = 2018
    day = 21

    def solve_puzzles(self):
        processor = ChronoProcessor(INSTRUCION_POINTER)
        processor.load_instructions(self.load_all_input_lines())

        processor.run_until_instruction(R0_COMPARE_INSTRUCTION)
        ans_one = processor.registers[5]

        value = None
        seen_values = set()
        processor.reset()
        while True:
            # Next Value by Instructions
            # processor.run_until_instruction(R0_COMPARE_INSTRUCTION)
            # processor.execute_current_instruction()

            # Next Value by Translation
            self._run_translation(processor.registers)

            next_value = processor.registers[5]

            if next_value in seen_values:
                break
            value = next_value
            seen_values.add(value)

        ans_two = value

        return ans_one, ans_two

    def _run_translation(self, registers):
        registers[4] = registers[5] | 65536
        registers[5] = 15466939

        while True:
            registers[3] = registers[4] & 255
            registers[5] += registers[3]
            registers[5] &= 16777215
            registers[5] *= 65899
            registers[5] &= 16777215

            if 256 > registers[4]:
                return

            registers[4] = registers[3] = registers[4] // 256
