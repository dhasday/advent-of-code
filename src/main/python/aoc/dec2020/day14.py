import re
from collections import defaultdict

from aoc.common.day_solver import DaySolver
from aoc.common.helpers import binary_to_decimal, decimal_to_binary

MASK_REGEX = re.compile(r'mask = ([01X]+)')
MEM_REGEX = re.compile(r'mem\[(\d+)\] = (\d+)')

LEN_MASK = 36


class Day14Solver(DaySolver):
    year = 2020
    day = 14

    def solve_puzzle_one(self):
        lines = self.load_all_input_lines()

        mask = None
        mem = defaultdict(lambda: 0)
        for line in lines:
            result = MASK_REGEX.match(line)
            if result:
                mask = result.group(1)
                continue

            result = MEM_REGEX.match(line)
            addr = result.group(1)
            value = int(result.group(2))
            mem[addr] = self._apply_mask(mask, value)

        return sum(mem.values())

    def solve_puzzle_two(self):
        lines = self.load_all_input_lines()

        mask = None
        mem = defaultdict(lambda: 0)
        for line in lines:
            result = MASK_REGEX.match(line)
            if result:
                mask = result.group(1)
                continue

            result = MEM_REGEX.match(line)
            addr = int(result.group(1))
            value = int(result.group(2))

            target_addrs = self._get_target_addrs(mask, decimal_to_binary(addr, LEN_MASK))
            for target_addr in target_addrs:
                mem[target_addr] = value

        return sum(mem.values())

    def _apply_mask(self, mask, value):
        bin_value = decimal_to_binary(value, LEN_MASK)

        applied = ''
        for i in range(LEN_MASK):
            if mask[i] == 'X':
                applied += bin_value[i]
            else:
                applied += mask[i]

        return binary_to_decimal(applied)

    def _get_target_addrs(self, mask, value):
        out = str(value)
        dual_bits = []
        for i in range(LEN_MASK):
            mask_val = mask[i]
            if mask_val == '1':
                out = out[0:i] + '1' + out[i + 1:]
            elif mask_val == 'X':
                out = out[0:i] + 'X' + out[i + 1:]
                dual_bits.append(i)

        return self._expand_addresses(out, dual_bits)

    def _expand_addresses(self, value, dual_bits):
        if len(dual_bits) == 0:
            return [binary_to_decimal(value)]

        bit = dual_bits[0]
        out = []

        out.extend(self._expand_addresses(value[0:bit] + '0' + value[bit + 1:], dual_bits[1:]))
        out.extend(self._expand_addresses(value[0:bit] + '1' + value[bit + 1:], dual_bits[1:]))

        return out
