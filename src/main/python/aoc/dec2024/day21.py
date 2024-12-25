from functools import cache

from aoc.common.day_solver import DaySolver

BUTTON_PATHS = {
    'A': {
        '1': '^<<A',
        '8': '<^^^A',
    },
    '0': {
        'A': '>A',
        '2': '^A',
        '3': '^>A',
    },
    '1': {
        '2': '>A',
        '4': '^A',
        '6': '^>>A',
        '7': '^^A',
    },
    '2': {
        '9': '^^>A',
    },
    '3': {
        'A': 'vA',
        '7': '<<^^A',
    },
    '4': {
        '0': '>vvA',
        '5': '>A',
    },
    '5': {
        '6': '>A',
    },
    '6': {
        'A': 'vvA',
        '9': '^A',
    },
    '7': {
        '0': '>vvvA',
        '9': '>>A',
    },
    '8': {
        '0': 'vvvA',
    },
    '9': {
        'A': 'vvvA',
        '8': '<A',
    },
}

DIRECTION_PATHS = {
    'A': {
        'A': 'A',
        '^': '<A',
        'v': '<vA',
        '<': 'v<<A',
        '>': 'vA',
    },
    '^': {
        'A': '>A',
        '^': 'A',
        'v': 'vA',
        '<': 'v<A',
        '>': 'v>A',
    },
    'v': {
        'A': '^>A',
        '^': '^A',
        'v': 'A',
        '<': '<A',
        '>': '>A',
    },
    '<': {
        'A': '>>^A',
        '^': '>^A',
        'v': '>A',
        '<': 'A',
        '>': '>>A',
    },
    '>': {
        'A': '^A',
        '^': '<^A',
        'v': '<A',
        '<': '<<A',
        '>': 'A',
    },
}


class Day21Solver(DaySolver):
    year = 2024
    day = 21

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        total_complexity_p1 = 0
        total_complexity_p2 = 0
        for line in lines:
            path_numpad = self._find_path(BUTTON_PATHS, line)

            total_keys_pressed_p1 = 0
            total_keys_pressed_p2 = 0
            prev_key = 'A'
            for cur_key in path_numpad:
                total_keys_pressed_p1 += self._expand_key_press(prev_key, cur_key, 2)
                total_keys_pressed_p2 += self._expand_key_press(prev_key, cur_key, 25)
                prev_key = cur_key

            total_complexity_p1 += total_keys_pressed_p1 * int(line[:-1])
            total_complexity_p2 += total_keys_pressed_p2 * int(line[:-1])

        return total_complexity_p1, total_complexity_p2

    def _find_path(self, mapping, line):
        path = ''
        prev_char = 'A'
        for cur_char in line:
            path += mapping[prev_char][cur_char]
            prev_char = cur_char
        return path

    @cache
    def _expand_key_press(self, prev_key, cur_key, num_times):
        if num_times == 0:
            return 1

        needed_presses = DIRECTION_PATHS[prev_key][cur_key]

        total_presses = 0
        prev = 'A'
        for cur in needed_presses:
            total_presses += self._expand_key_press(prev, cur, num_times - 1)
            prev = cur
        return total_presses
