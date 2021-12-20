from collections import Counter

from aoc.common.day_solver import DaySolver
from aoc.common.helpers import binary_to_decimal


class Day20Solver(DaySolver):
    year = 2021
    day = 20

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        enhancement = lines[0].replace('#', '1').replace('.', '0')
        image = [line.replace('#', '1').replace('.', '0') for line in lines[2:]]

        for i in range(2):
            image = self._enhance_image(enhancement, image, i % 2 == 0)
        part_1 = self._count_ones(image)

        for i in range(2, 50):
            image = self._enhance_image(enhancement, image, i % 2 == 0)
        part_2 = self._count_ones(image)

        return part_1, part_2

    def _enhance_image(self, enhancement, image, is_even):
        full_image = self._expand_image(image, is_even)

        output_image = []
        for y in range(1, len(full_image) - 1):
            output_line = ''
            for x in range(1, len(full_image[0]) - 1):
                lookup = full_image[y-1][x-1:x+2] + full_image[y][x-1:x+2] + full_image[y+1][x-1:x+2]
                output_line += enhancement[binary_to_decimal(lookup)]
            output_image.append(output_line)

        return output_image

    def _expand_image(self, image, is_even):
        expanded_length = len(image[0]) + 4

        # The background toggles on/off, so need to know what char to fill with
        enhancement_char = '0' if is_even else '1'

        # Expand the image by 2 in all directions to account for the new node
        full_image = [enhancement_char * expanded_length] * 2
        for line in image:
            full_image.append((enhancement_char * 2) + line + (enhancement_char * 2))
        full_image.extend([enhancement_char * expanded_length] * 2)

        return full_image

    def _count_ones(self, image):
        ctr = Counter(''.join(image))
        return ctr['1']
