import math
import re

from aoc.common.day_solver import DaySolver

INPUT_REGEX = re.compile(r'(\d+ [A-Z]+)')


class Day14Solver(DaySolver):
    year = 2019
    day = 14

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        parsed = [self._parse_line(line) for line in lines]
        reactions = {p[1][1]: (p[0], p[1][0]) for p in parsed}

        ans_one = self._get_ore_count(reactions, 1)

        target_ore = 1000000000000
        min_cnt = 0
        max_cnt = target_ore

        while min_cnt < max_cnt:
            mid = (min_cnt + max_cnt) // 2
            ore_cnt = self._get_ore_count(reactions, mid)
            if ore_cnt > target_ore:
                max_cnt = mid - 1
            else:
                min_cnt = mid

        return ans_one, min_cnt

    def _parse_line(self, line):
        operations = [o.split(' ') for o in INPUT_REGEX.findall(line)]
        operations = [(int(o[0]), o[1]) for o in operations]

        return operations[:-1], operations[-1]

    def _get_ore_count(self, reactions, fuel_cnt):
        required = {'FUEL': fuel_cnt}

        ore_cnt = 0
        while any(required[key] > 0 for key in required):
            element = [k for k in required if required[k] > 0][0]
            required_num = required[element]
            reaction_out_num = reactions[element][1]
            num_reactions = math.ceil(required_num / reaction_out_num)
            required[element] -= reaction_out_num * num_reactions

            for part in reactions[element][0]:
                quantity = part[0] * num_reactions
                component = part[1]

                if component == 'ORE':
                    ore_cnt += quantity
                else:
                    if component not in required:
                        required[component] = 0

                    required[component] += quantity

        return ore_cnt
