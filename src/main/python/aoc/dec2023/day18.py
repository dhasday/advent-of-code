from aoc.common.day_solver import DaySolver


DIR_OFFSETS = {
    '0': (0, 1), 'R': (0, 1),
    '1': (1, 0), 'D': (1, 0),
    '2': (0, -1), 'L': (0, -1),
    '3': (-1, 0), 'U': (-1, 0),
}


class Day18Solver(DaySolver):
    year = 2023
    day = 18

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        p1_cur_location = p2_cur_location = 0, 0
        p1_perimeter = p2_perimeter = 0
        p1_corners = []
        p2_corners = []

        for line in lines:
            split_line = line.split(' ')

            p1_distance = int(split_line[1])
            p1_offset = DIR_OFFSETS.get(split_line[0])
            p1_cur_location = self._apply_offset(p1_cur_location, p1_offset, p1_distance)
            p1_corners.append(p1_cur_location)
            p1_perimeter += p1_distance

            p2_distance = int(split_line[2][2:7], 16)
            p2_offset = DIR_OFFSETS.get(split_line[2][7])
            p2_cur_location = self._apply_offset(p2_cur_location, p2_offset, p2_distance)
            p2_corners.append(p2_cur_location)
            p2_perimeter += p2_distance

        ans_one = self._shoelace_area(p1_corners, p1_perimeter)
        ans_two = self._shoelace_area(p2_corners, p2_perimeter)

        return ans_one, ans_two

    def _apply_offset(self, pos, offset, distance):
        return pos[0] + (offset[0] * distance), pos[1] + (offset[1] * distance)

    def _shoelace_area(self, corners, perimeter):
        """https://en.wikipedia.org/wiki/Shoelace_formula"""
        total_area = 0
        for i in range(len(corners)):
            total_area += (corners[i - 1][1] + corners[i][1]) * (corners[i - 1][0] - corners[i][0])

        # Need to also include the other half of the perimeter
        return abs(total_area) // 2 + (perimeter // 2) + 1
