from collections import defaultdict

from aoc.common.day_solver import DaySolver


def move_north(elves, elf):
    nw = (elf[0] - 1, elf[1] - 1) in elves
    n = (elf[0], elf[1] - 1) in elves
    ne = (elf[0] + 1, elf[1] - 1) in elves

    if not (nw or n or ne):
        return elf[0], elf[1] - 1


def move_south(elves, elf):
    se = (elf[0] + 1, elf[1] + 1) in elves
    s = (elf[0], elf[1] + 1) in elves
    sw = (elf[0] - 1, elf[1] + 1) in elves

    if not (sw or s or se):
        return elf[0], elf[1] + 1


def move_west(elves, elf):
    nw = (elf[0] - 1, elf[1] - 1) in elves
    w = (elf[0] - 1, elf[1]) in elves
    sw = (elf[0] - 1, elf[1] + 1) in elves

    if not (nw or w or sw):
        return elf[0] - 1, elf[1]


def move_east(elves, elf):
    ne = (elf[0] + 1, elf[1] - 1) in elves
    e = (elf[0] + 1, elf[1]) in elves
    se = (elf[0] + 1, elf[1] + 1) in elves

    if not (ne or e or se):
        return elf[0] + 1, elf[1]


ALL_TESTS = [
    move_north,
    move_south,
    move_west,
    move_east,
]


class Day23Solver(DaySolver):
    year = 2022
    day = 23

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        elves = set()
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                if c == '#':
                    elves.add((x, y))

        dir_tests = ALL_TESTS[:]

        for _ in range(10):
            elves, dir_tests = self.simulate_round(elves, dir_tests)

        min_x, max_x, min_y, max_y = self._get_bounds(elves)
        p1 = (max_y - min_y + 1) * (max_x - min_x + 1) - len(elves)

        cur_round = 10
        any_moved = True
        while any_moved:
            cur_round += 1
            next_elves, dir_tests = self.simulate_round(elves, dir_tests)

            if next_elves == elves:
                break
            elves = next_elves

        return p1, cur_round

    def simulate_round(self, current_elves, dir_tests):
        moves = defaultdict(list)
        for elf in current_elves:
            target = self._get_target(current_elves, elf, dir_tests)
            moves[target].append(elf)

        new_elves = set()
        for target, elves in moves.items():
            if len(elves) == 1:
                new_elves.add(target)
            else:
                new_elves.update(elves)

        dir_tests = dir_tests[1:] + [dir_tests[0]]

        return new_elves, dir_tests

    def _get_target(self, current_elves, elf, dir_tests):
        has_neighbor = False
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if (elf[0] + i, elf[1] + j) in current_elves:
                    has_neighbor = True
                    break
            if has_neighbor:
                break
        if not has_neighbor:
            return elf

        for test in dir_tests:
            next_elf = test(current_elves, elf)
            if next_elf is not None:
                return next_elf
        return elf

    def _get_bounds(self, elves):
        min_x, min_y = max_x, max_y = next(iter(elves))
        for elf in elves:
            min_x = min(min_x, elf[0])
            max_x = max(max_x, elf[0])
            min_y = min(min_y, elf[1])
            max_y = max(max_y, elf[1])
        return min_x, max_x, min_y, max_y
