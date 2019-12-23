import math

from aoc.common.day_solver import DaySolver


class Day10Solver(DaySolver):
    year = 2019
    day = 10

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        asteroids = set()
        for y, row in enumerate(lines):
            for x, val in enumerate(row):
                if val == '#':
                    asteroids.add((x, y))

        max_visible = None
        max_point = None
        max_slopes = None
        for asteroid in asteroids:
            all_slopes = self._map_slopes(asteroids, asteroid)
            visible = len(all_slopes)

            if max_visible is None or visible > max_visible:
                max_visible = visible
                max_point = asteroid
                max_slopes = all_slopes

        last_point = self._destroy_n_asteroids(max_slopes, max_point, 200)
        ans_two = (last_point[0] * 100) + last_point[1]

        return max_visible, ans_two

    def _map_slopes(self, asteroids, a1):
        all_slopes = {}

        for a2 in asteroids:
            if a2 == a1:
                continue

            dx = a1[0] - a2[0]
            dy = a1[1] - a2[1]
            gcd = math.gcd(dx, dy)

            slope = dx // gcd, dy // gcd
            if slope not in all_slopes:
                all_slopes[slope] = set()
            all_slopes[slope].add(a2)

        return all_slopes

    def _destroy_n_asteroids(self, all_slopes, point, n):
        sorted_slopes = sorted(all_slopes.keys(), key=self._slope_to_degrees)
        final_slope = all_slopes[sorted_slopes[199]]
        return sorted(final_slope, key=lambda p: self._distance(point, p))[0]

    def _slope_to_degrees(self, slope):
        ang = math.atan2(slope[0], slope[1])
        # atan2 wraps around from +pi to -pi
        # we'd rather it wrapped from 2pi to 0
        if ang < 0:
            ang += 2 * math.pi
        # atan2 goes counterclockwise
        # lets reverse that
        # 0 is a special case
        if ang != 0:
            ang = 2 * math.pi - ang
        return ang

    def _distance(self, p1, p2):
        return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])

