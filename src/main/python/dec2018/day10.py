import re

from common.day_solver import DaySolver


INPUT_REGEX = re.compile('position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>')


class Day10Solver(DaySolver):
    year = 2018
    day = 10

    class Light(object):
        def __init__(self, line):
            parsed = INPUT_REGEX.match(line)

            self.position = int(parsed.group(1)), int(parsed.group(2))
            self.velocity = int(parsed.group(3)), int(parsed.group(4))

        def advance_light(self, times=1):
            self.position = self.position[0] + (self.velocity[0] * times), self.position[1] + (self.velocity[1] * times)

    class Bounds(object):
        min_x = None
        max_x = None

        min_y = None
        max_y = None

        size_x = 0
        size_y = 0
        offset_x = 0
        offset_y = 0

        def compute_size(self):
            self.size_x = min(self.max_x - self.min_x + 2, 1001)
            self.size_y = min(self.max_y - self.min_y + 2, 1001)

        def compute_offset(self):
            self.offset_x = max(self.min_x, -500)
            self.offset_y = max(self.min_y, -500)

        def append_point(self, x, y):
            if self.min_x is None or x < self.min_x:
                self.min_x = x

            if self.max_x is None or x > self.max_x:
                self.max_x = x

            if self.min_y is None or y < self.min_y:
                self.min_y = y

            if self.max_y is None or y > self.max_y:
                self.max_y = y

    def solve_puzzles(self):
        lights = self._load_lights()

        bounds = self._determine_bounds(lights)

        # Input positions seemed to be about velocity * 10000, so just accelerate the processing a bit
        initial_offset = 10000
        for l in lights:
            l.advance_light(initial_offset)

        ans_two = None
        for i in range(1000):
            for l in lights:
                l.advance_light()
            if self._print_lights(lights, bounds):
                ans_two = initial_offset + i + 1
                break

        return 'READ OUTPUT', ans_two

    def _load_lights(self):
        return [self.Light(l) for l in self._load_all_input_lines()]

    def _determine_bounds(self, lights):
        bounds = self.Bounds()

        for l in lights:
            (x, y) = l.position
            bounds.append_point(x, y)

        bounds.compute_size()
        bounds.compute_offset()

        return bounds

    def _print_lights(self, lights, bounds):

        grid = [' ' * bounds.size_x for _ in range(bounds.size_y)]

        relevant_bounds = self.Bounds()

        num_in_range = 0
        for l in lights:
            pos_x = l.position[0] - bounds.offset_x
            pos_y = l.position[1] - bounds.offset_y

            if pos_x < 0 or pos_x >= bounds.size_x or pos_y < 0 or pos_y >= bounds.size_y:
                continue

            relevant_bounds.append_point(pos_x, pos_y)

            grid_line = grid[pos_y]
            grid[pos_y] = grid_line[:pos_x] + '#' + grid_line[pos_x + 1:]
            num_in_range += 1

        # Text height is 10 characters
        if num_in_range > 5 and relevant_bounds.max_y - relevant_bounds.min_y == 9:
            print ''
            for l in range(relevant_bounds.min_y, relevant_bounds.max_y + 1):
                line = grid[l]
                print line[relevant_bounds.min_x:relevant_bounds.max_x + 1]
            print ''
            return True
        return False
