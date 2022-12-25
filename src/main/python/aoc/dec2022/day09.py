from aoc.common.day_solver import DaySolver


DIRECTION_DELTA = {
    'U': (0, 1),
    'D': (0, -1),
    'L': (-1, 0),
    'R': (1, 0),
}


class Day09Solver(DaySolver):
    year = 2022
    day = 9

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        rope = [[0, 0] for _ in range(10)]

        p1_visited = {tuple(rope[1])}
        p2_visited = {tuple(rope[-1])}
        for line in lines:
            direction, distance = line.split(' ')
            distance = int(distance)
            for i in range(distance):
                rope[0][0] += DIRECTION_DELTA[direction][0]
                rope[0][1] += DIRECTION_DELTA[direction][1]

                for j in range(1, len(rope)):
                    dx = rope[j][0] - rope[j - 1][0]
                    dy = rope[j][1] - rope[j - 1][1]
                    dist = dx * dy
                    if dist < 0:
                        dist *= -1

                    if dist > 1 or (dist == 0 and (dx > 1 or dx < -1)):
                        rope[j][0] -= 1 if dx > 0 else -1
                    if dist > 1 or (dist == 0 and (dy > 1 or dy < -1)):
                        rope[j][1] -= 1 if dy > 0 else -1

                p1_visited.add(tuple(rope[1]))
                p2_visited.add(tuple(rope[-1]))

        return len(p1_visited), len(p2_visited)
