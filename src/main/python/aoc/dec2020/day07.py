import re
from collections import defaultdict

from aoc.common.day_solver import DaySolver


INPUT_REGEX = re.compile(r'([a-z ]+) bags contain ([a-z0-9 ,]+).')
INNER_COLOR_REGEX = re.compile(r'\s*(\d+) ([a-z ]+) bag\.*')

TARGET_COLOR = 'shiny gold'


class Day07Solver(DaySolver):
    year = 2020
    day = 7

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        containing_bags = defaultdict(lambda: set())
        bag_contents = {}

        for line in lines:
            outer, inner = self._parse_line(line)
            bag_contents[outer] = inner
            for color in inner:
                containing_bags[color].add(outer)

        ans_one = self._count_containing_colors(containing_bags, TARGET_COLOR)
        # Remove one since we don't want to count the outer bag
        ans_two = self._count_total_contained_bags(bag_contents, TARGET_COLOR) - 1

        return ans_one, ans_two

    def _parse_line(self, line):
        result = INPUT_REGEX.match(line)
        outer_color = result.group(1)
        inner_colors = {}

        for inner_bag in INNER_COLOR_REGEX.findall(result.group(2)):
            num, color = inner_bag
            inner_colors[color] = int(num)

        return outer_color, inner_colors

    def _count_containing_colors(self, bags, target):
        to_check = set()
        to_check.add(target)

        seen = set()
        while to_check:
            cur = to_check.pop()
            for c in bags[cur]:
                if c not in seen:
                    to_check.add(c)
                seen.add(c)

        return len(seen)

    def _count_total_contained_bags(self, bag_contents, color):
        total_count = 1

        for bag, count in bag_contents[color].items():
            num_nested_bags = self._count_total_contained_bags(bag_contents, bag)
            total_count += (num_nested_bags * count)

        return total_count
