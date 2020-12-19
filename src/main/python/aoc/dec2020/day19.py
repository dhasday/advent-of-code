from aoc.common.day_solver import DaySolver


class Day19Solver(DaySolver):
    year = 2020
    day = 19

    def solve_puzzles(self):
        rules_part1 = self._load_rules()

        rules_part2 = rules_part1.copy()
        rules_part2[8] = [[42], [42, 8]]
        rules_part2[11] = [[42, 31], [42, 11, 31]]

        messages = self.load_all_input_lines(filename='19-input-2')
        reversed_base_rule = list(reversed(rules_part1[0][0]))

        ans_one = 0
        ans_two = 0
        for message in messages:
            if self._matches_rule_stack(rules_part1, reversed_base_rule.copy(), message):
                ans_one += 1
            if self._matches_rule_stack(rules_part2, reversed_base_rule.copy(), message):
                ans_two += 1

        return ans_one, ans_two

    def _load_rules(self):
        lines = self.load_all_input_lines(filename='19-input-1')

        all_rules = {}
        for line in lines:
            num, rule_str = line.split(': ')

            rules = []
            for rule in rule_str.split(' | '):
                option = []
                for char in rule.split(' '):
                    if char.isnumeric():
                        option.append(int(char))
                    else:
                        option.append(char)
                rules.append(option)
            all_rules[int(num)] = rules

        return all_rules

    def _matches_rule_stack(self, all_rules, rule_stack, message):
        if len(rule_stack) > len(message):
            return False
        if len(rule_stack) == 0 and len(message) == 0:
            return True
        if len(rule_stack) == 0 or len(message) == 0:
            return False

        char = rule_stack.pop()
        if isinstance(char, int):
            for rule in all_rules[char]:
                if self._matches_rule_stack(all_rules, rule_stack + list(reversed(rule)), message):
                    return True
        elif message[0] == char:
            return self._matches_rule_stack(all_rules, rule_stack.copy(), message[1:])

        return False
