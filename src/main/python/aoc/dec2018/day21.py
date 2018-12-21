from aoc.common.day_solver import DaySolver
from aoc.dec2018.common.chronal_assembly import ChronalAssembly

INSTRUCION_POINTER = 2
R0_COMPARE_INSTRUCTION = 28


class Day21Solver(DaySolver):
    year = 2018
    day = 21

    def solve_puzzles(self):
        chronal_assembly = ChronalAssembly(INSTRUCION_POINTER)
        chronal_assembly.load_instructions(self._load_all_input_lines())

        chronal_assembly.run_until_instruction(R0_COMPARE_INSTRUCTION)
        ans_one = chronal_assembly.registers[5]

        # ans_two = self._ans_two_by_instructions(chronal_assembly)
        ans_two = self._ans_two_by_translation()

        return ans_one, ans_two

    def _ans_two_by_instructions(self, chronal_assembly):
        seen_values = set()
        chronal_assembly.reset()

        while True:
            chronal_assembly.run_until_instruction(R0_COMPARE_INSTRUCTION)
            chronal_assembly.execute_current_instruction()
            next_value = chronal_assembly.registers[5]
            if next_value in seen_values:
                break
            value = next_value
            seen_values.add(value)

        return value

    def _ans_two_by_translation(self):
        seen_values = set()
        registers = [0] * 6
        while True:
            self._run_translation(registers)
            if registers[5] in seen_values:
                break
            value = registers[5]
            seen_values.add(value)

        return value

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

            registers[4] = registers[3] = registers[4] / 256
