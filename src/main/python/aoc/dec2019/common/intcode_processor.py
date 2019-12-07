def noop(*args): return None


def inc_ptr(num): return lambda ptr, *args: ptr + num


class Operation(object):
    def __init__(self, opcode, arity, has_output, get_value, get_next_ctr):
        self.opcode = opcode
        self.arity = arity
        self.has_output = has_output
        self.get_value = get_value
        self.get_next_ctr = get_next_ctr


OPERATION_MAP = {
    1: Operation(1, 3, True, lambda i, a, b, c: a + b, inc_ptr(4)),
    2: Operation(2, 3, True, lambda i, a, b, c: a * b, inc_ptr(4)),
    3: Operation(3, 1, True, lambda i, a: i, inc_ptr(2)),
    4: Operation(4, 1, False, lambda i, a: a, inc_ptr(2)),
    5: Operation(5, 2, False, noop, lambda ptr, i, a, b: b if a != 0 else ptr + 3),
    6: Operation(6, 2, False, noop, lambda ptr, i, a, b: b if a == 0 else ptr + 3),
    7: Operation(7, 3, True, lambda i, a, b, c: 1 if a < b else 0, inc_ptr(4)),
    8: Operation(8, 3, True, lambda i, a, b, c: 1 if a == b else 0, inc_ptr(4)),
}


class IntcodeProcessor(object):
    program = [99]
    ctr = 0
    last_output = None
    last_opcode = None

    def __init__(self, program_str, input_value=0):
        self._program = [int(v) for v in program_str.split(',')]
        self.input_value = input_value

        self.reset()

    def reset(self):
        self.program = self._program[:]
        self.ctr = 0
        self.last_output = None
        self.last_opcode = None

    def run_until_instruction(self, target_opcode):
        opcode = None
        while opcode != target_opcode:
            instruction = self.program[self.ctr]

            opcode = instruction % 100
            self.last_opcode = opcode
            if opcode == 99:
                return

            operation = OPERATION_MAP.get(opcode)
            if not operation:
                raise Exception('Unable to execute opcode {}'.format(opcode))

            args = self._get_args(operation.arity, operation.has_output)

            result = operation.get_value(self.input_value, *args)
            if operation.has_output:
                self.program[args[-1]] = result
            elif opcode == 4:
                self.last_output = result

            self.ctr = operation.get_next_ctr(self.ctr, self.input_value, *args)

    def run_until_completion(self):
        self.run_until_instruction(99)

    def _get_args(self, num_args, has_output):
        modes = self.program[self.ctr] // 100

        args = []
        for i in range(num_args):
            arg = self.program[self.ctr + i + 1]

            is_output_arg = has_output and i + 1 == num_args

            if not is_output_arg:
                mode = modes % 10
                if mode == 0:
                    arg = self.program[arg]
                elif mode != 1:
                    raise Exception('arg mode {} not supported'.format(mode))

            modes //= 10
            args.append(arg)

        return args
