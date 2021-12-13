from collections import defaultdict, deque

from aoc.common.day_solver import DaySolver
from aoc.common.letter_reader import read_output, read_output_from_points


class Day13Solver(DaySolver):
    year = 2021
    day = 13

    def solve_puzzles(self):
        points, instructions = self._load_input()

        points = self._process_instruction(points, instructions[0])
        part_1 = len(points)

        for ins in instructions[1:]:
            points = self._process_instruction(points, ins)
        part_2 = read_output_from_points(points, 40, 6)

        return part_1, part_2

    def _load_input(self):
        points = set()
        instructions = []

        add_point = True
        for line in self.load_all_input_lines():
            if line == '':
                add_point = False
            elif add_point:
                a, b = line.split(',')
                points.add((int(a), int(b)))
            else:
                a, b = line.split(' ')[2].split('=')
                instructions.append((a, int(b)))

        return points, instructions

    def _process_instruction(self, points, instruction):
        new_points = set()
        if instruction[0] == 'x':
            for point in points:
                if point[0] < instruction[1]:
                    new_points.add(point)
                elif point[0] > instruction[1]:
                    new_x = instruction[1] - (point[0] - instruction[1])
                    new_points.add((new_x, point[1]))
        else:
            for point in points:
                if point[1] < instruction[1]:
                    new_points.add(point)
                elif point[1] > instruction[1]:
                    new_y = instruction[1] - (point[1] - instruction[1])
                    new_points.add((point[0], new_y))

        return new_points
