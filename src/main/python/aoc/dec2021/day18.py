import math
from collections import defaultdict, deque

from aoc.common.day_solver import DaySolver
from aoc.common.helpers import ALL_NUMBERS_REGEX


class Day18Solver(DaySolver):
    year = 2021
    day = 18

    def solve_puzzle_one(self):
        lines = self.load_all_input_lines()

        all_numbers = [self.parse_line(line) for line in lines]

        total = all_numbers[0]
        for num in all_numbers[1:]:
            total += num

        return total.magnitude()

    def solve_puzzle_two(self):
        lines = self.load_all_input_lines()

        magnitudes = set()
        for line_1 in lines:
            for line_2 in lines:
                if line_1 == line_2:
                    continue
                num_1 = self.parse_line(line_1)
                num_2 = self.parse_line(line_2)
                total = num_1 + num_2
                magnitudes.add(total.magnitude())
        return max(magnitudes)

    def parse_line(self, line):
        num, _ = self._parse_line(line)
        return num

    def _parse_line(self, line, start_idx=0, parent=None):
        number = SnailNumber(parent=parent)
        cur_pos = start_idx + 1
        while cur_pos < len(line):
            cur_val = line[cur_pos]

            if cur_val == '[':
                subnumber, cur_pos = self._parse_line(line, cur_pos, number)
            elif cur_val in ',]':
                cur_pos += 1
                continue
            else:
                subnumber = int(line[cur_pos])
                cur_pos += 1

            if number.left is None:
                number.left = subnumber
            else:
                number.right = subnumber
                return number, cur_pos

        return 'ERROR', 'ERROR'


class SnailNumber(object):
    def __init__(self, left=None, right=None, parent=None):
        self.left = left
        self.right = right
        self.parent = parent

    def __repr__(self):
        return '[{},{}]'.format(self.left, self.right)

    def __add__(self, other):
        result = self.__class__(self, other)
        self.parent = result
        other.parent = result
        result.reduce()
        return result

    def magnitude(self):
        if isinstance(self.left, self.__class__):
            total = 3 * self.left.magnitude()
        else:
            total = 3 * self.left

        if isinstance(self.right, self.__class__):
            total += 2 * self.right.magnitude()
        else:
            total += 2 * self.right

        return total

    def reduce(self):
        while True:
            if self._explode():
                continue
            if self._split():
                continue
            return

    def _explode(self, cur_depth=1):
        if isinstance(self.left, self.__class__):
            if cur_depth == 4:
                self.left._do_explode()
                self.left = 0
                return True
            elif self.left._explode(cur_depth + 1):
                return True
        if isinstance(self.right, self.__class__):
            if cur_depth == 4:
                self.right._do_explode()
                self.right = 0
                return True
            elif self.right._explode(cur_depth + 1):
                return True
        return False

    def _do_explode(self):
        left_target, is_left = self._find_left_target()
        if left_target is not None:
            if is_left:
                left_target.left += self.left
            else:
                left_target.right += self.left

        right_target, is_left = self._find_right_target()
        if right_target is not None:
            if is_left:
                right_target.left += self.right
            else:
                right_target.right += self.right

        return False

    def _find_left_target(self):
        cur_node = self
        while cur_node.parent and cur_node == cur_node.parent.left:
            cur_node = cur_node.parent

        if not cur_node.parent:
            return None, None

        search_node = cur_node.parent.left
        if isinstance(search_node, int):
            return cur_node.parent, True

        while not isinstance(search_node.right, int):
            search_node = search_node.right

        return search_node, False

    def _find_right_target(self):
        cur_node = self
        while cur_node.parent and cur_node == cur_node.parent.right:
            cur_node = cur_node.parent

        if not cur_node.parent:
            return None, None

        search_node = cur_node.parent.right
        if isinstance(search_node, int):
            return cur_node.parent, False

        while not isinstance(search_node.left, int):
            search_node = search_node.left

        return search_node, True

    def _split(self):
        did_split = False
        if isinstance(self.left, int):
            if self.left > 9:
                self.left = self._do_split(self.left)
                did_split = True
        elif self.left._split():
            did_split = True

        if did_split:
            return True

        if isinstance(self.right, int):
            if self.right > 9:
                self.right = self._do_split(self.right)
                did_split = True
        elif self.right._split():
            did_split = True

        return did_split

    def _do_split(self, value):
        left_val = value // 2
        right_val = left_val + 1 if value % 2 == 1 else left_val
        return self.__class__(left_val, right_val, self)
