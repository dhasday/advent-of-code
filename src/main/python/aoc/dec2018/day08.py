import re

from aoc.common.day_solver import DaySolver

INPUT_REGEX = re.compile('')


class Day08Solver(DaySolver):
    year = 2018
    day = 8

    class Node(object):
        def __init__(self, parent=None):
            self.parent = parent
            self.children = []
            self.metadata = []

        def metadata_total(self):
            total = self._sum_metadata()

            for c in self.children:
                total += c.metadata_total()

            return total

        def node_value(self):
            if not self.children:
                return self._sum_metadata()

            total = 0
            for m in self.metadata:
                if m <= len(self.children):
                    total += self.children[m - 1].node_value()

            return total

        def _sum_metadata(self):
            total = 0

            for m in self.metadata:
                total += m

            return total

    def solve_puzzles(self):
        values = [int(v) for v in self._load_only_input_line().split(' ')]

        root_node, _ = self._build_node(values=values, parent=None)

        ans_one = root_node.metadata_total()
        ans_two = root_node.node_value()

        return ans_one, ans_two

    def _build_node(self, values, parent=None):
        num_children = values[0]
        num_metadata = values[1]
        node = self.Node(parent)

        cur_index = 2
        for i in range(num_children):
            child, node_length = self._build_node(values[cur_index:], node)

            node.children.append(child)
            cur_index += node_length

        next_index = cur_index + num_metadata
        node.metadata = values[cur_index:next_index]

        return node, next_index
