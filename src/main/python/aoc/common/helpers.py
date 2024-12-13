import math
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

STANDARD_DIRECTIONS_3D_MANHATTAN = [
    (-1, 0, 0),
    (1, 0, 0),
    (0, -1, 0),
    (0, 1, 0),
    (0, 0, -1),
    (0, 0, 1),
]

STANDARD_DIRECTIONAL_OFFSETS_3D = [
    (-1, -1, -1),
    (-1, -1, 0),
    (-1, -1, 1),
    (-1, 0, -1),
    (-1, 0, 0),
    (-1, 0, 1),
    (-1, 1, -1),
    (-1, 1, 0),
    (-1, 1, 1),
    (0, -1, -1),
    (0, -1, 0),
    (0, -1, 1),
    (0, 0, -1),
    (0, 0, 0),
    (0, 0, 1),
    (0, 1, -1),
    (0, 1, 0),
    (0, 1, 1),
    (1, -1, -1),
    (1, -1, 0),
    (1, -1, 1),
    (1, 0, -1),
    (1, 0, 0),
    (1, 0, 1),
    (1, 1, -1),
    (1, 1, 0),
    (1, 1, 1),
]

HEX_DIRECTION_OFFSETS = {
    'e': lambda p: (p[0] - 1, p[1] + 1, p[2]),
    'se': lambda p: (p[0], p[1] + 1, p[2] - 1),
    'sw': lambda p: (p[0] + 1, p[1], p[2] - 1),
    'w': lambda p: (p[0] + 1, p[1] - 1, p[2]),
    'nw': lambda p: (p[0], p[1] - 1, p[2] + 1),
    'ne': lambda p: (p[0] - 1, p[1], p[2] + 1),
}


def parse_all_numbers(line):
    return [int(v) for v in ALL_NUMBERS_REGEX.findall(line)]

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


def split_layers(full_output, layer_size):
    """Splits a single list into layers of the specified size"""
    for i in range(0, len(full_output), layer_size):
        yield full_output[i:i + layer_size]


def lcm(values):
    _lcm = values[0]
    for v in values[1:]:
        gcd = math.gcd(_lcm, v)
        _lcm = abs(_lcm * v) // gcd

    return _lcm


def apply_deltas(point, deltas):
    return tuple(v + deltas[i] for i, v in enumerate(point))


def manhattan_distance(p1, p2):
    distance = 0
    for i in range(len(p1)):
        distance += abs(p1[i] - p2[i])
    return distance
