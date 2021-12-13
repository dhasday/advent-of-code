from aoc.common.day_solver import DaySolver
from aoc.dec2019.common.intcode_processor import IntcodeProcessor
from aoc.common.letter_reader import read_output


class Day11Solver(DaySolver):
    year = 2019
    day = 11

    class Bounds:
        min_x = None
        min_y = None

        def load(self, points):
            self.min_x = min(points, key=lambda p: p[0])[0]
            self.min_y = min(points, key=lambda p: p[1])[1]

        def build_grid(self, points):
            size_x = 40
            size_y = 6

            grid = [' ' * size_x] * size_y
            for point in points:
                x = point[0] - self.min_x
                y = point[1] - self.min_y
                grid[y] = grid[y][:x] + '0' + grid[y][x + 1:]
            grid.reverse()
            return grid

    def solve_puzzle_one(self):
        line = self.load_only_input_line()

        processor = IntcodeProcessor(line)

        white_spots = set()
        painted_spots = set()

        cur_spot = 0, 0

        self._run_robot(processor, cur_spot, white_spots, painted_spots)

        return len(painted_spots)

    def solve_puzzle_two(self):
        line = self.load_only_input_line()

        processor = IntcodeProcessor(line)

        white_spots = set()
        painted_spots = set()

        cur_spot = 0, 0
        white_spots.add(cur_spot)

        self._run_robot(processor, cur_spot, white_spots, painted_spots)

        bounds = self.Bounds()
        bounds.load(white_spots)
        grid = bounds.build_grid(white_spots)

        return read_output(grid)

    def _run_robot(self, processor, cur_spot, white_spots, painted_spots):
        direction = 0, 1

        processor.input_func = lambda: 1 if cur_spot in white_spots else 0
        while True:
            # Update color
            output = processor.get_next_output()
            if processor.last_opcode == 99:
                break
            painted_spots.add(cur_spot)
            if output == 1:
                white_spots.add(cur_spot)
            else:
                white_spots.discard(cur_spot)

            # Turn & move
            output = processor.get_next_output()
            if processor.last_opcode == 99:
                break
            if output == 0:
                direction = - direction[1], direction[0]
            else:
                direction = direction[1], - direction[0]
            cur_spot = cur_spot[0] + direction[0], cur_spot[1] + direction[1]
