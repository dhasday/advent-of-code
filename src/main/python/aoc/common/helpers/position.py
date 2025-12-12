import math

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


def manhattan_distance(p1, p2):
    distance = 0
    for i in range(len(p1)):
        distance += abs(p1[i] - p2[i])
    return distance


def get_manhattan_circle_offsets(radius):
    offsets = set()
    for cur_radius in range(radius + 1):
        x, y = (cur_radius, radius - cur_radius)
        # print(x, y)
        offsets.update([(x, y), (x, -y), (-x, -y), (-x, y)])
    return offsets


def euclidean_distance(p1, p2):
    distance = 0
    for i in range(len(p1)):
        distance += math.pow(abs(p1[i] - p2[i]), 2)
    return math.sqrt(distance)

def apply_deltas(point, deltas):
    return tuple(v + deltas[i] for i, v in enumerate(point))
