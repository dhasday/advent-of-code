from aoc.common.day_solver import DaySolver

DIR_UP = '^'
DIR_DOWN = 'v'
DIR_LEFT = '<'
DIR_RIGHT = '>'

DIRECTION_OFFSETS = {
    DIR_UP: (0, -1),
    DIR_DOWN: (0, 1),
    DIR_LEFT: (-1, 0),
    DIR_RIGHT: (1, 0),
}

CURVE_NEXT_DIRS = {
    '/': {
        DIR_UP: DIR_RIGHT,
        DIR_DOWN: DIR_LEFT,
        DIR_LEFT: DIR_DOWN,
        DIR_RIGHT: DIR_UP,
    },
    '\\': {
        DIR_UP: DIR_LEFT,
        DIR_DOWN: DIR_RIGHT,
        DIR_LEFT: DIR_UP,
        DIR_RIGHT: DIR_DOWN,
    }
}

INTERSECTION_NEXT_DIRS = {
    0: {
        DIR_UP: DIR_LEFT,
        DIR_DOWN: DIR_RIGHT,
        DIR_LEFT: DIR_DOWN,
        DIR_RIGHT: DIR_UP,
    },
    1: {
        DIR_UP: DIR_UP,
        DIR_DOWN: DIR_DOWN,
        DIR_LEFT: DIR_LEFT,
        DIR_RIGHT: DIR_RIGHT,
    },
    2: {
        DIR_UP: DIR_RIGHT,
        DIR_DOWN: DIR_LEFT,
        DIR_LEFT: DIR_UP,
        DIR_RIGHT: DIR_DOWN,
    },
}


class Day13Solver(DaySolver):
    year = 2018
    day = 13

    junctions = {}

    class Cart(object):
        intersection_count = 0

        def __init__(self, x, y, token):
            self.pos = (x, y)
            self.dir = token

        def move_cart(self):
            pos_offset = DIRECTION_OFFSETS[self.dir]

            next_pos = self.pos[0] + pos_offset[0], self.pos[1] + pos_offset[1]

            if next_pos in Day13Solver.junctions:
                token = Day13Solver.junctions[next_pos]
                if token in CURVE_NEXT_DIRS:
                    self.dir = CURVE_NEXT_DIRS[token][self.dir]
                else:  # We're at an intersection
                    self.dir = INTERSECTION_NEXT_DIRS[self.intersection_count][self.dir]
                    self.intersection_count = (self.intersection_count + 1) % 3

            self.pos = next_pos

            if next_pos[0] < 0 or next_pos[1] < 0 or next_pos[0] > 200 or next_pos[1] > 200:
                raise Exception('You dun goofed somewhere')

            return self.pos

        def __str__(self):
            return '{} {}'.format(self.pos, self.dir)

    def solve_puzzle_one(self):
        carts = self._load_input()

        collision_pos = None
        while not collision_pos:
            collision_pos = self._move_carts_for_first_collision(carts)

        return '{},{}'.format(collision_pos[0], collision_pos[1])

    def solve_puzzle_two(self):
        carts = self._load_input()

        while len(carts) > 1:
            carts, collided_carts = self._move_carts_for_all_collisions(carts)
            for c in collided_carts:
                carts.remove(c)

        if len(carts) != 1:
            return 'ERROR'

        return '{},{}'.format(carts[0].pos[0], carts[0].pos[1])

    def _load_input(self):
        carts = list()

        for y, line in enumerate(self._load_all_input_lines()):
            for x, token in enumerate(line):
                if token in ['/', '\\', '+']:
                    self.junctions[(x, y)] = token
                elif token in ['>', '<', '^', 'v']:
                    carts.append(self.Cart(x, y, token))

        return carts

    def _move_carts_for_first_collision(self, carts):
        carts = sorted(carts, key=(lambda c: c.pos))

        seen_pos = set()

        for cart in carts:
            if cart.pos in seen_pos:
                return cart.pos

            next_pos = cart.move_cart()

            if next_pos in seen_pos:
                return next_pos

            seen_pos.add(next_pos)

        return None

    def _move_carts_for_all_collisions(self, carts):
        carts = sorted(carts, key=(lambda c: c.pos))

        seen_pos = {}
        carts_to_remove = set()

        for cart in carts:
            if cart.pos in seen_pos:
                carts_to_remove.add(seen_pos[cart.pos])
                carts_to_remove.add(cart)
                continue

            next_pos = cart.move_cart()

            if next_pos in seen_pos:
                carts_to_remove.add(seen_pos[cart.pos])
                carts_to_remove.add(cart)
                continue

            seen_pos[next_pos] = cart

        return carts, carts_to_remove
