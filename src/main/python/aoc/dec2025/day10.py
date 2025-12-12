from collections import defaultdict

from z3 import Int, Optimize

from aoc.common import helpers
from aoc.common.breadth_first_search import BreadthFirstSearch
from aoc.common.day_solver import DaySolver


class Day10Solver(DaySolver):
    year = 2025
    day = 10

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        light_pushes = 0
        digit_pushes = 0
        for line in lines:
            parts = line.split(' ')
            light_target = tuple(p == '#' for p in parts[0][1:-1])
            digit_target = tuple(helpers.parse_all_numbers(parts[-1][1:-1]))

            buttons = []
            for part in parts[1:-1]:
                buttons.append(helpers.parse_all_numbers(part))

            light_pushes += self._get_min_pushes_lights(light_target, buttons)
            digit_pushes += self._get_min_pushes_joltage(digit_target, buttons)

        return light_pushes, digit_pushes

    def _get_min_pushes_lights(self, target, buttons):
        # TODO: Maybe optimize this by converting target and buttons to bit so they can be xor instead of looping
        num_lights = len(target)
        def find_adjacent_nodes(current):
            adj = []
            for button in buttons:
                next_value = tuple(
                    not current[v] if v in button else current[v]
                    for v in range(num_lights)
                )
                adj.append(next_value)
            return adj

        bfs = BreadthFirstSearch(find_adjacent_nodes)

        start = tuple([False] * len(target))

        path = bfs.find_path(start, target)

        return len(path) - 1

    def _get_min_pushes_joltage(self, target, buttons):
        total_presses = Int('p')
        buttons_vars = [Int(f'b{i}') for i in range(len(buttons))]

        # Build a map of digit to buttons that change it
        digit_buttons = defaultdict(list)
        for i, button in enumerate(buttons):
            for digit in button:
                digit_buttons[digit].append(i)

        optimize = Optimize()

        # Add an equation for each digit where value = sum of applicable button presses
        for digit, applicable_buttons in digit_buttons.items():
            optimize.add(target[digit] == sum([buttons_vars[i] for i in applicable_buttons]))
        # Add a constraint that each button must have a non-negative number of pushes
        for button_var in buttons_vars:
            optimize.add(button_var >= 0)
        # Equation to get the output result of total presses
        optimize.add(total_presses == sum(buttons_vars))

        # Set the target to minimize total presses and solve
        optimize.minimize(total_presses)
        optimize.check()
        return int(str(optimize.model()[total_presses]))
