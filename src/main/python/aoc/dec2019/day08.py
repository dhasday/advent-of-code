from aoc.common.day_solver import DaySolver
from aoc.common.letter_reader import read_output

LAYER_WIDTH = 25
LAYER_HEIGHT = 6
LAYER_SIZE = LAYER_HEIGHT * LAYER_WIDTH


class Day08Solver(DaySolver):
    year = 2019
    day = 8

    def solve_puzzle_one(self):
        line = self.load_only_input_line()

        layers = list(self.split_layers(line, LAYER_SIZE))

        min_zeros = None
        result = None

        for layer in layers:
            counts = self._count_layer(layer)

            if min_zeros is None or counts['0'] < min_zeros:
                min_zeros = counts['0']
                result = int(counts['1']) * int(counts['2'])

        return result

    def solve_puzzle_two(self):
        line = self.load_only_input_line()

        layer_size = LAYER_HEIGHT * LAYER_WIDTH

        layers = list(self.split_layers(line, layer_size))

        output = [self._determine_color(layers, i) for i in range(layer_size)]

        lines = [''.join(l) for l in self.split_layers(output, 25)]
        return read_output(lines)

    def split_layers(self, lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    def _count_layer(self, layer):
        counts = {
            '0': 0,
            '1': 0,
            '2': 0,
        }

        for v in layer:
            counts[v] += 1

        return counts

    def _determine_color(self, layers, index):
        for layer in layers:
            val = layer[index]
            if val != '2':
                return ' ' if val == '0' else '0'
        return ' '
