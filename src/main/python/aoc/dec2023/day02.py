import re

from aoc.common.day_solver import DaySolver


RED = 'red'
GREEN = 'green'
BLUE = 'blue'

GAME_REGEX = re.compile(r'Game (\d+):')
COUNT_REGEX = re.compile(r'(\d+ [a-z]+)')


class Day02Solver(DaySolver):
    year = 2023
    day = 2

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        ans_one = 0
        ans_two = 0
        for line in lines:
            game_num, red, green, blue = self._get_min_required_for_game(line)

            if red <= 12 and green <= 13 and blue <= 14:
                ans_one += game_num
            ans_two += (red * green * blue)

        return ans_one, ans_two

    def _get_min_required_for_game(self, line):
        game_number = int(GAME_REGEX.match(line)[1])
        red = blue = green = None

        for color_count in COUNT_REGEX.findall(line):
            count = int(color_count.split(' ')[0])
            if color_count.endswith(RED):
                red = max(red, count) if red else count
            elif color_count.endswith(GREEN):
                green = max(green, count) if green else count
            elif color_count.endswith(BLUE):
                blue = max(blue, count) if blue else count

        return game_number, red, green, blue
