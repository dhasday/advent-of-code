from common.day_solver import DaySolver


class Day16Solver(DaySolver):
    year = 2018
    day = 16

    class Instruction(object):
        def __init__(self, instruction):
            parsed = instruction.split(' ')

            self.code = int(parsed[0])
            self.input_one = int(parsed[1])
            self.input_two = int(parsed[2])
            self.output = int(parsed[3])

        def _addr(self, cur_registers):  # Add registers
            op_result = cur_registers[self.input_one] + cur_registers[self.input_two]
            return self._generate_output(cur_registers, op_result)

        def _addi(self, cur_registers):  # Add immediate
            op_result = cur_registers[self.input_one] + self.input_two
            return self._generate_output(cur_registers, op_result)

        def _mulr(self, cur_registers):  # Multiple Registers
            op_result = cur_registers[self.input_one] * cur_registers[self.input_two]
            return self._generate_output(cur_registers, op_result)

        def _muli(self, cur_registers):  # Multiple Immediate
            op_result = cur_registers[self.input_one] * self.input_two
            return self._generate_output(cur_registers, op_result)

        def _banr(self, cur_registers):  # Binary And Registers
            op_result = cur_registers[self.input_one] & cur_registers[self.input_two]
            return self._generate_output(cur_registers, op_result)

        def _bani(self, cur_registers):  # Binary And Immediate
            op_result = cur_registers[self.input_one] & self.input_two
            return self._generate_output(cur_registers, op_result)

        def _borr(self, cur_registers):  # Binary Or Registers
            op_result = cur_registers[self.input_one] | cur_registers[self.input_two]
            return self._generate_output(cur_registers, op_result)

        def _bori(self, cur_registers):  # Binary Or Immediate
            op_result = cur_registers[self.input_one] | self.input_two
            return self._generate_output(cur_registers, op_result)

        def _setr(self, cur_registers):  # Set Registers
            return self._generate_output(cur_registers, cur_registers[self.input_one])

        def _seti(self, cur_registers):  # Set Immediate
            return self._generate_output(cur_registers, self.input_one)

        def _gtir(self, cur_registers):  # Greater Than Immediate Register
            op_result = 1 if self.input_one > cur_registers[self.input_two] else 0
            return self._generate_output(cur_registers, op_result)

        def _gtri(self, cur_registers):  # Greater Than Register Immediate
            op_result = 1 if cur_registers[self.input_one] > self.input_two else 0
            return self._generate_output(cur_registers, op_result)

        def _gtrr(self, cur_registers):  # Greater Than Registers
            op_result = 1 if cur_registers[self.input_one] > cur_registers[self.input_two] else 0
            return self._generate_output(cur_registers, op_result)

        def _eqir(self, cur_registers):  # Equals Immediate Register
            op_result = 1 if self.input_one == cur_registers[self.input_two] else 0
            return self._generate_output(cur_registers, op_result)

        def _eqri(self, cur_registers):  # Equals Register Immediate
            op_result = 1 if cur_registers[self.input_one] == self.input_two else 0
            return self._generate_output(cur_registers, op_result)

        def _eqrr(self, cur_registers):  # Equals Registers
            op_result = 1 if cur_registers[self.input_one] == cur_registers[self.input_two] else 0
            return self._generate_output(cur_registers, op_result)

        def _generate_output(self, cur_registers, op_result):
            output = cur_registers[::]
            output[self.output] = op_result
            return output

    def solve_puzzles(self):
        part_one_input, part_two_input = self._load_input()
        ans_one, opcodes = self._solve_part_one(part_one_input)
        ans_two = self._solve_part_two(part_two_input, opcodes)
        return ans_one, ans_two

    def _load_input(self):
        filename = self._get_input_filename()

        part_one_input = []
        part_two_input = []

        with open(filename) as f:
            start_registers = None
            instruction = None
            for line in f:
                line = line.strip('\n')
                if not line:
                    continue
                elif 'Before' in line:
                    start_registers = [int(r) for r in line[:-1].split('[')[1].split(', ')]
                elif 'After' in line:
                    end_registers = [int(r) for r in line[:-1].split('[')[1].split(', ')]
                    part_one_input.append([start_registers, instruction, end_registers])
                    start_registers = None
                else:
                    instruction = self.Instruction(line)
                    if not start_registers:
                        part_two_input.append(instruction)

        return part_one_input, part_two_input

    def _solve_part_one(self, samples):
        instruction_methods = [
            '_addr', '_addi', '_mulr', '_muli', '_banr', '_bani', '_borr', '_bori',
            '_setr', '_seti', '_gtir', '_gtri', '_gtrr', '_eqri', '_eqir', '_eqrr',
        ]

        ans_one = 0
        opcodes = {}
        for s in samples:
            start_registers, instruction, end_registers = s

            if instruction.code not in opcodes:
                opcodes[instruction.code] = set()

            matching_count = 0
            for m in instruction_methods:
                op_result = getattr(instruction, m)(start_registers)
                if op_result == end_registers:
                    matching_count += 1
                    opcodes[instruction.code].add(m)

            if matching_count >= 3:
                ans_one += 1

        return ans_one, opcodes

    def _solve_part_two(self, instructions, opcodes):
        opcode_map = {}
        while len(opcode_map) < 16:
            for code in opcodes:
                if code in opcode_map:
                    continue

                cur_codes = opcodes[code].difference(opcode_map.values())
                if len(cur_codes) == 1:
                    opcode_map[code] = cur_codes.pop()

        registers = [0, 0, 0, 0]
        for instruction in instructions:
            registers = getattr(instruction, opcode_map[instruction.code])(registers)

        return registers[0]
