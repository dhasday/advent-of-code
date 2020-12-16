import re
from collections import defaultdict

from aoc.common.day_solver import DaySolver

INPUT_REGEX_FIELDS = re.compile(r'([a-z ]+): (\d+)-(\d+) or (\d+)-(\d+)')


class Day16Solver(DaySolver):
    year = 2020
    day = 16

    def solve_puzzles(self):
        fields, my_ticket, nearby_tickets = self._load_input()

        error_rate, valid_tickets = self._validate_tickets(fields, nearby_tickets)
        ans_one = error_rate

        field_order = self._determine_field_order(fields, valid_tickets)
        ans_two = 1
        for field, idx in field_order.items():
            if field.startswith('departure'):
                ans_two *= my_ticket[idx]

        return ans_one, ans_two

    def _load_input(self):
        fields = {}
        for line in self.load_all_input_lines(filename='16-input-1'):
            result = INPUT_REGEX_FIELDS.match(line)
            fields[result.group(1)] = [
                (int(result.group(2)), int(result.group(3))),
                (int(result.group(4)), int(result.group(5))),
            ]

        my_ticket = [int(n) for n in self.load_only_input_line(filename='16-input-2').split(',')]

        nearby_tickets = []
        for line in self.load_all_input_lines(filename='16-input-3'):
            nearby_tickets.append([int(n) for n in line.split(',')])

        return fields, my_ticket, nearby_tickets

    def _validate_tickets(self, fields, nearby_tickets):
        error_rate = 0
        valid_tickets = []
        for ticket in nearby_tickets:
            is_valid = True
            for num in ticket:
                if not self._matches_any_field(fields, num):
                    is_valid = False
                    error_rate += num
            if is_valid:
                valid_tickets.append(ticket)
        return error_rate, valid_tickets

    def _matches_any_field(self, fields, value):
        for field in fields.items():
            if self._is_valid_for_field(field, value):
                return True
        return False

    def _is_valid_for_field(self, field, value):
        r1, r2 = field[1]
        return r1[0] <= value <= r1[1] or r2[0] <= value <= r2[1]

    def _determine_field_order(self, fields, valid_tickets):
        values_by_index = defaultdict(lambda: list())
        for ticket in valid_tickets:
            for idx, num in enumerate(ticket):
                values_by_index[idx].append(num)

        possibilities = {}
        for field in fields.items():
            field_possibilities = set()
            for i in range(len(values_by_index)):
                if self._is_field_valid_for_all_values(field, values_by_index[i]):
                    field_possibilities.add(i)
            possibilities[field[0]] = field_possibilities

        # Sort the keys by the number of valid possibilities since looking at the data showed that
        # if you go from most to least restricted then the first path is the correct one
        remaining_keys = sorted(possibilities.items(), key=lambda p: len(p[1]))
        remaining_keys = [k for k, v in remaining_keys]

        return self._find_valid_configuration(
            possibilities,
            remaining_keys,
            {},
            list(range(len(fields))),
        )

    def _is_field_valid_for_all_values(self, field, values):
        low_one, high_one = field[1][0]
        low_two, high_two = field[1][1]
        for value in values:
            if not (low_one <= value <= high_one or low_two <= value <= high_two):
                return False
        return True

    def _find_valid_configuration(self, possibilities, remaining_keys, assignments, remaining_values):
        if len(remaining_keys) == 0:
            return assignments

        cur_key = remaining_keys[0]
        taken_values = set(assignments.values())
        for possibility in possibilities[cur_key]:
            if possibility in taken_values:
                continue

            new_assignments = assignments.copy()
            new_assignments[cur_key] = possibility
            new_values = remaining_values.copy()
            new_values.remove(possibility)
            new_assignments = self._find_valid_configuration(
                possibilities,
                remaining_keys[1:],
                new_assignments,
                new_values,
            )
            if new_assignments is not None:
                return new_assignments

        return None
