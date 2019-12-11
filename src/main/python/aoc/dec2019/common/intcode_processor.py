class IntcodeProcessor(object):
    program = [99]
    ctr = 0
    relative_base = 0
    last_output = None
    last_opcode = None
    program_length = 0

    def __init__(self, program_str, input_value=0):
        self._program = [int(v) for v in program_str.split(',')]
        self.input_value = input_value

        self.reset()

        self.OPERATION_MAP = {
            1: self._add,
            2: self._multiply,
            3: self._input,
            4: self._output,
            5: self._jump_if_true,
            6: self._jump_if_false,
            7: self._less_than,
            8: self._equal,
            9: self._adjust_relative_base,
        }

    def reset(self):
        self.program = self._program[:]
        self.ctr = 0
        self.relative_base = 0
        self.last_output = None
        self.last_opcode = None
        self.program_length = len(self.program)

    def get_program_value(self, index):
        self._ensure_program_addessable(index)
        return self.program[index]

    def set_program_value(self, index, value):
        self._ensure_program_addessable(index)
        self.program[index] = value

    def _ensure_program_addessable(self, index):
        if index < 0:
            raise Exception('Can\'t access negative index')

        if index > self.program_length - 1:
            self.program.extend([0] * (index - self.program_length + 1))

    def stop_after_instruction(self, target_opcode):
        opcode = None
        while opcode != target_opcode:
            opcode = self.get_next_opcode()
            self.last_opcode = opcode
            if opcode == 99:
                return

            self.execute_current_step()

    def run_to_completion(self):
        self.stop_after_instruction(99)

    def execute_current_step(self, input_value=None):
        if input_value is not None:
            self.input_value = input_value

        opcode = self.get_next_opcode()
        if opcode == 99:
            return

        operation = self.OPERATION_MAP.get(opcode)
        if not operation:
            raise Exception('Unable to execute opcode {}'.format(opcode))
        operation()

    def get_next_opcode(self):
        instruction = self.get_program_value(self.ctr)
        return instruction % 100

    def _get_args(self, num_args, has_output):
        modes = self.get_program_value(self.ctr) // 100

        args = []
        for i in range(num_args):
            arg = self.get_program_value(self.ctr + i + 1)

            is_output_arg = has_output and i + 1 == num_args

            mode = modes % 10
            if not is_output_arg:
                if not is_output_arg and mode == 0:
                    arg = self.get_program_value(arg)
                elif mode == 2:
                    arg = self.get_program_value(arg + self.relative_base)
                elif mode != 1:
                    raise Exception('arg mode {} not supported'.format(mode))
            else:
                if mode == 2:
                    arg += self.relative_base

            modes //= 10
            args.append(arg)

        return args

    def _add(self):
        args = self._get_args(3, True)

        result = args[0] + args[1]
        self.set_program_value(args[2], result)
        self.ctr += 4

    def _multiply(self):
        args = self._get_args(3, True)

        result = args[0] * args[1]
        self.set_program_value(args[2], result)
        self.ctr += 4

    def _input(self):
        args = self._get_args(1, True)

        self.set_program_value(args[0], self.input_value)
        self.ctr += 2

    def _output(self):
        args = self._get_args(1, False)

        # print('OUT: {}'.format(args[0]))
        self.last_output = args[0]
        self.ctr += 2

    def _jump_if_true(self):
        args = self._get_args(2, False)

        if args[0] != 0:
            self.ctr = args[1]
        else:
            self.ctr += 3

    def _jump_if_false(self):
        args = self._get_args(2, False)

        if args[0] == 0:
            self.ctr = args[1]
        else:
            self.ctr += 3

    def _less_than(self):
        args = self._get_args(3, True)

        result = 1 if args[0] < args[1] else 0
        self.set_program_value(args[2], result)
        self.ctr += 4

    def _equal(self):
        args = self._get_args(3, True)

        result = 1 if args[0] == args[1] else 0
        self.set_program_value(args[2], result)
        self.ctr += 4

    def _adjust_relative_base(self):
        args = self._get_args(1, False)

        self.relative_base += args[0]
        self.ctr += 2
