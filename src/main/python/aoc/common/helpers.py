import re

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
