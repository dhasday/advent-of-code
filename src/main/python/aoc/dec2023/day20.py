import dataclasses
import math
from collections import deque
from enum import Enum
from typing import List, Dict

from aoc.common.day_solver import DaySolver

BROADCASTER_NAME = 'broadcaster'


class OperationType(Enum):
    BROADCASTER = 1
    FLIP_FLOP = 2
    CONJUNCTION = 3


@dataclasses.dataclass
class Operation:
    name: str
    outputs: List[str]


class Broadcaster(Operation):
    op_type = OperationType.BROADCASTER

    def pulse(self, signal):
        return signal.value


class FlipFlop(Operation):
    op_type = OperationType.FLIP_FLOP
    state = False

    def pulse(self, signal):
        if signal.value is True:
            return None

        self.state = not self.state
        return self.state


class Conjunction(Operation):
    op_type = OperationType.CONJUNCTION
    last_inputs: Dict[str, int]

    def register_inputs(self, all_operations):
        self.last_inputs = {}
        for operation in all_operations:
            if self.name in operation.outputs:
                self.last_inputs[operation.name] = False

    def pulse(self, signal):
        self.last_inputs[signal.from_name] = signal.value
        for value in self.last_inputs.values():
            if value is False:
                return True
        return False


@dataclasses.dataclass
class Signal:
    from_name: str
    to_name: str
    value: bool

    def __repr__(self):
        return f'{self.from_name} -{"high" if self.value else "low"}-> {self.to_name}'


class Day20Solver(DaySolver):
    year = 2023
    day = 20

    operations = None

    def setup(self):
        lines = self.load_all_input_lines()

        self.operations = {}
        for line in lines:
            label, outputs = line.replace(" ", "").replace("-", "").split('>')
            outputs = outputs.split(",")

            if label == BROADCASTER_NAME:
                self.operations[label] = Broadcaster(name=label, outputs=outputs)
            elif label[0] == '%':
                label = label[1:]
                self.operations[label] = FlipFlop(name=label, outputs=outputs)
            elif label[0] == '&':
                label = label[1:]
                self.operations[label] = Conjunction(name=label, outputs=outputs)
            else:
                raise Exception('Failed to match operation')

        for operation in self.operations.values():
            if operation.op_type == OperationType.CONJUNCTION:
                operation.register_inputs(self.operations.values())

    def solve_puzzle_one(self):
        initial_signal = Signal(from_name='button', to_name=BROADCASTER_NAME, value=False)

        low_count = 0
        high_count = 0
        for i in range(1000):
            to_send = deque()
            to_send.append(initial_signal)
            while to_send:
                cur_signal = to_send.popleft()

                if cur_signal.value is True:
                    high_count += 1
                elif cur_signal.value is False:
                    low_count += 1

                cur_operation = self.operations.get(cur_signal.to_name)
                if cur_operation is None:
                    continue
                result = cur_operation.pulse(cur_signal)
                if result is not None:
                    for output in cur_operation.outputs:
                        to_send.append(Signal(from_name=cur_operation.name, to_name=output, value=result))

        return low_count * high_count

    def solve_puzzle_two(self):
        initial_signal = Signal(from_name='button', to_name=BROADCASTER_NAME, value=False)
        target = 'rx'

        target_op = None
        for operation in self.operations.values():
            if target in operation.outputs:
                target_op = operation
                break
        assert target_op is not None

        input_cycles = {n: [] for n in target_op.last_inputs.keys()}

        for i in range(10000):
            to_send = deque()
            to_send.append(initial_signal)
            while to_send:
                cur_signal = to_send.popleft()

                cur_operation = self.operations.get(cur_signal.to_name)
                if cur_operation is None:
                    continue
                result = cur_operation.pulse(cur_signal)
                if cur_operation.name in input_cycles and result is True:
                    input_cycles[cur_operation.name].append(i + 1)

                if result is not None:
                    for output in cur_operation.outputs:
                        to_send.append(Signal(from_name=cur_operation.name, to_name=output, value=result))

        if target_op.op_type == OperationType.CONJUNCTION:
            return math.lcm(*[c[1] - c[0] for c in input_cycles.values()])
        else:
            return min(c[0] for c in input_cycles.values())
