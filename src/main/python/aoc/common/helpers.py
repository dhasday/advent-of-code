import re

ALL_DIGITS_REGEX = re.compile(r'\d+')
ALL_NUMBERS_REGEX = re.compile(r'-?\d+')

STANDARD_DIRECTIONS = [
    (1, 0),   # Right
    (0, -1),  # Down
    (-1, 0),  # Left
    (0, 1),   # Up
]

VERTICAL_FLIPPED_DIRECTIONS = [
    (1, 0),  # Right
    (0, 1),  # Down
    (-1, 0),  # Left
    (0, -1),  # Up
]

STANDARD_DIRECTIONAL_OFFSETS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]

HEX_DIRECTION_OFFSETS = {
    'e': lambda p: (p[0] - 1, p[1] + 1, p[2]),
    'se': lambda p: (p[0], p[1] + 1, p[2] - 1),
    'sw': lambda p: (p[0] + 1, p[1], p[2] - 1),
    'w': lambda p: (p[0] + 1, p[1] - 1, p[2]),
    'nw': lambda p: (p[0], p[1] - 1, p[2] + 1),
    'ne': lambda p: (p[0] - 1, p[1], p[2] + 1),
}


def decimal_to_binary(value, min_length=None):
    result = ''

    cur_value = value
    while cur_value > 0:
        result = str(cur_value % 2) + result
        cur_value //= 2

    if min_length:
        result = result.zfill(min_length)

    return result


def binary_to_decimal(value):
    return int(value, 2)


def hex_to_binary(value):
    out = str(bin(int(value, 16)))[2:]
    missing = len(out) % 8
    if missing:
        out = '0' * (8-missing) + out
    return out
