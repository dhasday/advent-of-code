from collections import defaultdict
from functools import cmp_to_key

from aoc.common.day_solver import DaySolver


class Day05Solver(DaySolver):
    year = 2024
    day = 5

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        split_idx = lines.index('')
        rules = defaultdict(set)
        for line in lines[0:split_idx]:
            v1, v2 = line.split('|')
            rules[v1].add(v2)

        cmp = cmp_to_key(lambda x, y:  y not in rules[x])
        total_p1 = 0
        total_p2 = 0
        for manual in lines[split_idx + 1:]:
            pages = manual.split(',')

            if self._is_valid(rules, pages):
                total_p1 += int(pages[len(pages) // 2])
            else:
                reordered = sorted(pages, key=cmp)
                total_p2 += int(reordered[len(reordered) // 2])

        return total_p1, total_p2

    def _is_valid(self, rules, manual):
        for idx, val in enumerate(manual):
            before = rules[val]
            if before.intersection(manual[:idx]):
                return False

        return True
