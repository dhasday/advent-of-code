from aoc.common.day_solver import DaySolver

PART_TWO_MAX_DISTANCE = 10000


class Day06Solver(DaySolver):
    year = 2018
    day = 6

    def solve_puzzle_one(self):
        points = self._load_input()
        min_x, max_x, min_y, max_y = self._determine_bounds(points)

        size_x = max_x - min_x + 1
        size_y = max_y - min_y + 1

        infinite_areas = self._find_infinite_areas(points, size_x, size_y)

        area_sizes = [0 for _ in points]
        max_size = 0
        for x in range(1, size_x - 1):
            for y in range(1, size_y - 1):
                closest = self._find_closest_point(points, x + min_x, y + min_y)
                if closest is not None and closest not in infinite_areas:
                    area_sizes[closest] += 1
                    if area_sizes[closest] > max_size:
                        max_size = area_sizes[closest]

        return max_size

    def solve_puzzle_two(self):
        points = self._load_input()

        min_x, max_x, min_y, max_y = self._determine_bounds(points)

        count_within_distance = 0
        for x in range(min_x, max_x + 1):
            # TODO: Need to think about it a bit more, but this might not work for all inputs
            first_y = self._find_first_y_within_distance(points, x, min_y, max_y + 1, 1)
            if first_y is not None:
                last_y = self._find_first_y_within_distance(points, x, max_y + 1, first_y, -1)
                if last_y is None:
                    last_y = first_y
                count_within_distance += (last_y - first_y + 1)

        return count_within_distance

    def _load_input(self):
        return [self._load_line(l) for l in self.load_all_input_lines()]

    def _load_line(self, line):
        result = line.split(', ')
        return int(result[0]), int(result[1])

    def _determine_bounds(self, points):
        min_x = points[0][0]
        max_x = points[0][0]
        min_y = points[0][1]
        max_y = points[0][1]

        for (x, y) in points:
            if min_x > x:
                min_x = x
            elif max_x < x:
                max_x = x

            if min_y > y:
                min_y = y
            elif max_y < y:
                max_y = y

        return min_x, max_x, min_y, max_y

    def _find_closest_point(self, points, x, y):
        closest_point = None
        closest_distance = None

        for i in range(len(points)):
            point = points[i]
            distance = abs(point[0] - x) + abs(point[1] - y)

            if closest_distance is None or distance < closest_distance:
                closest_point = i
                closest_distance = distance
            elif distance == closest_distance:
                closest_point = None

        return closest_point

    def _find_infinite_areas(self, points, size_x, size_y):
        infinite_areas = set()
        for y in range(size_y):
            controller = self._find_closest_point(points, 0, y)
            if controller is not None:
                infinite_areas.add(controller)

            controller = self._find_closest_point(points, size_x - 1, y)
            if controller is not None:
                infinite_areas.add(controller)

        for x in range(size_x):
            controller = self._find_closest_point(points, x, 0)
            if controller is not None:
                infinite_areas.add(controller)

            controller = self._find_closest_point(points, x, size_y - 1)
            if controller is not None:
                infinite_areas.add(controller)

        return infinite_areas

    def _find_first_y_within_distance(self, points, x, y_start, y_end, y_step):
        for y in range(y_start, y_end, y_step):
            if self._is_within_max_distance(points, PART_TWO_MAX_DISTANCE, x, y):
                return y

        return None

    def _is_within_max_distance(self, points, max_distance, x, y):
        total_distance = 0

        for (p_x, p_y) in points:
            total_distance += abs(p_x - x) + abs(p_y - y)
            if total_distance >= max_distance:
                return False

        return True
