class ThreeBitComputer:
    def __init__(self, reg_a, reg_b, reg_c, instructions):
        self._reg_a = reg_a
        self._reg_b = reg_b
        self._reg_c = reg_c

        self.reg_a = reg_a
        self.reg_b = reg_b
        self.reg_c = reg_c
        self.instructions = instructions
        self.ins_ptr = 0

    def reset(self, reg_a=None, reg_b=None, reg_c=None):
        self.reg_a = reg_a if reg_a is not None else self._reg_a
        self.reg_b = reg_b if reg_b is not None else self._reg_b
        self.reg_c = reg_c if reg_c is not None else self._reg_c
        self.ins_ptr = 0

    def process_next_instruction(self):
        opcode = self.instructions[self.ins_ptr]

        match opcode:
            case 0:
                return self.adv()
            case 1:
                return self.bxl()
            case 2:
                return self.bst()
            case 3:
                return self.jnz()
            case 4:
                return self.bxc()
            case 5:
                return self.out()
            case 6:
                return self.bdv()
            case 7:
                return self.cdv()

        raise Exception(f'Invalid opcode: {opcode}')

    def run_until_end(self):
        """Runs the program until it exists, returns list of outputs"""
        output = []
        while self.ins_ptr < len(self.instructions):
            out = self.process_next_instruction()
            if out is not None:
                output.append(out)
        return output

    def run_until_output(self):
        """Runs the program until it ends or outputs a value"""
        while self.ins_ptr < len(self.instructions):
            out = self.process_next_instruction()
            if out is not None:
                return out
        return None

    def adv(self):
        self.reg_a = int(self.reg_a // (2 ** self._get_combo_operand_value()))
        self.ins_ptr += 2

    def bxl(self):
        self.reg_b = self.reg_b ^ self._get_literal_operand()
        self.ins_ptr += 2

    def bst(self):
        self.reg_b = self._get_combo_operand_value() % 8
        self.ins_ptr += 2

    def jnz(self):
        if self.reg_a == 0:
            self.ins_ptr += 2
        else:
            self.ins_ptr = self._get_literal_operand()

    def bxc(self):
        self.reg_b = self.reg_b ^ self.reg_c
        self.ins_ptr += 2

    def out(self):
        result = int(self._get_combo_operand_value() % 8)
        self.ins_ptr += 2
        return result

    def bdv(self):
        self.reg_b = int(self.reg_a // (2 ** self._get_combo_operand_value()))
        self.ins_ptr += 2

    def cdv(self):
        self.reg_c = int(self.reg_a // (2 ** self._get_combo_operand_value()))
        self.ins_ptr += 2

    def _get_literal_operand(self):
        return self.instructions[self.ins_ptr + 1]

    def _get_combo_operand_value(self):
        literal = self._get_literal_operand()

        match literal:
            case 0 | 1 | 2 | 3:
                return literal
            case 4:
                return self.reg_a
            case 5:
                return self.reg_b
            case 6:
                return self.reg_c

        raise Exception(f'Invalid combo operand: {literal}')
