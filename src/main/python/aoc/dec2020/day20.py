import functools
import operator
from collections import defaultdict

from aoc.common.day_solver import DaySolver

TILE_SIZE = 10
GRID_SIZE = 12
MONSTER_LENGTH = 20

SIDE_TOP = 0
SIDE_RIGHT = 1
SIDE_BOTTOM = 2
SIDE_LEFT = 3


def rotate(image):
    rotated_values = list(zip(*image[::-1]))
    return [''.join(i) for i in rotated_values]


def flip(image):
    return [i[::-1] for i in image]


class Day20Solver(DaySolver):
    year = 2020
    day = 20

    class Tile(object):
        def __init__(self, id, lines):
            self.id = id
            self.lines = lines
            self._load_edges()

        def print_tile(self):
            for line in self.lines:
                print(line)

        def _load_edges(self):
            top = self.lines[0]
            bottom = self.lines[-1]

            left = ''
            right = ''
            for i in range(TILE_SIZE):
                left += self.lines[i][0]
                right += self.lines[i][-1]

            self.edges = [
                top, top[::-1],
                bottom, bottom[::-1],
                left, left[::-1],
                right, right[::-1],
            ]

        def get_side(self, side):
            if side == SIDE_TOP:
                return self.lines[0]
            elif side == SIDE_BOTTOM:
                return self.lines[-1]
            elif side == SIDE_LEFT:
                return ''.join(i[0] for i in self.lines)
            elif side == SIDE_RIGHT:
                return ''.join(i[-1] for i in self.lines)

            raise Exception('unknown side')

        def rotate(self):
            return self.__class__(self.id, rotate(self.lines))

        def flip(self):
            return self.__class__(self.id, flip(self.lines))

        def __hash__(self):
            return self.id

        def __eq__(self, other):
            return self.id == other.id

    def solve_puzzle_one(self):
        all_tiles = self._load_tiles()
        corner_tiles = self._find_corner_tiles(all_tiles)
        return functools.reduce(operator.mul, corner_tiles, 1)

    def solve_puzzle_two(self):
        all_tiles = self._load_tiles()

        start_tile = next(iter(all_tiles.values()))
        grid = self._find_grid(all_tiles, start_tile)
        image = self._expand_image(grid)

        num_monsters = self._find_max_monsters(image)
        return sum(line.count('#') for line in image) - (num_monsters * 15)

    def _load_tiles(self):
        all_tiles = {}

        cur_id = None
        cur_tile = []
        for line in self.load_all_input_lines():
            if line.startswith('Tile'):
                cur_id = int(line[5:9])
            elif line == '':
                all_tiles[cur_id] = self.Tile(cur_id, cur_tile)
                cur_tile = []
            else:
                cur_tile.append(line.replace('.', ' '))

        if cur_tile:
            all_tiles[cur_id] = self.Tile(cur_id, cur_tile)

        return all_tiles

    def _find_corner_tiles(self, all_tiles):
        unique_edges = defaultdict(lambda: 0)
        for tile in all_tiles.values():
            for e in tile.edges:
                unique_edges[e] += 1

        edge_patterns = {u for u in unique_edges if unique_edges[u] == 1}
        corner_tiles = set()
        for tile_id, tile in all_tiles.items():
            unmatched_edge_count = 0
            for e in tile.edges:
                if e in edge_patterns:
                    unmatched_edge_count += 1
            if unmatched_edge_count == 4:
                corner_tiles.add(tile_id)

        return corner_tiles

    def _find_grid(self, all_tiles, start_tile):
        placed_tiles = {
            start_tile: (0, 0),
        }

        to_check = set()
        to_check.add(start_tile)

        adjacent_checks = [
            (SIDE_TOP, SIDE_BOTTOM, 0, -1),
            (SIDE_BOTTOM, SIDE_TOP, 0, 1),
            (SIDE_LEFT, SIDE_RIGHT, -1, 0),
            (SIDE_RIGHT, SIDE_LEFT, 1, 0),
        ]
        while to_check:
            cur_tile = to_check.pop()
            cur_x, cur_y = placed_tiles.get(cur_tile)

            for next_tile in all_tiles.values():
                if next_tile in placed_tiles:
                    continue

                for cur_side, next_side, d_x, d_y in adjacent_checks:
                    expected_side = cur_tile.get_side(cur_side)

                    if expected_side in next_tile.edges:
                        rotated_tile = self._fix_orientation(next_tile, next_side, expected_side)
                        next_pos = cur_x + d_x, cur_y + d_y
                        placed_tiles[rotated_tile] = next_pos
                        to_check.add(rotated_tile)
                        break

        return {v: k for k, v in placed_tiles.items()}

    def _fix_orientation(self, tile, side, expected_value):
        if tile.get_side(side) == expected_value:
            return tile

        for _ in range(3):
            tile = tile.rotate()
            if tile.get_side(side) == expected_value:
                return tile

        tile = tile.flip()
        if tile.get_side(side) == expected_value:
            return tile

        for _ in range(3):
            tile = tile.rotate()
            if tile.get_side(side) == expected_value:
                return tile

        raise Exception('No matching orientation found')

    def _expand_image(self, grid):
        min_x = min(p[0] for p in grid.keys())
        max_x = max(p[0] for p in grid.keys())

        min_y = min(p[1] for p in grid.keys())
        max_y = max(p[1] for p in grid.keys())

        image = ['' for _ in range((TILE_SIZE - 2) * GRID_SIZE)]
        cur_row = 0
        for y in range(min_y, max_y + 1):
            for tile_line in range(1, TILE_SIZE - 1):
                for x in range(min_x, max_x + 1):
                    image[cur_row] += grid[x, y].lines[tile_line][1:TILE_SIZE - 1]

                cur_row += 1

        return image

    def _find_max_monsters(self, image):
        ops = [rotate, rotate, rotate, flip, rotate, rotate, rotate]

        max_monsters = self._find_monsters(image)
        for op in ops:
            image = op(image)
            monsters = self._find_monsters(image)
            max_monsters = max(max_monsters, monsters)
        return max_monsters

    def _find_monsters(self, image):
        count = 0
        for y in range(0, len(image) - 3):
            for x in range(0, len(image) - MONSTER_LENGTH):
                if self._does_shape_match(
                            image[y][x:x+MONSTER_LENGTH],
                            image[y+1][x:x+MONSTER_LENGTH],
                            image[y + 2][x:x + MONSTER_LENGTH],
                        ):
                    count += 1

        return count

    def _does_shape_match(self, *lines):
        # Sea Monster
        # |                  # |
        # |#    ##    ##    ###|
        # | #  #  #  #  #  #   |
        monster_shape = [
            (0, 18),
            (1, 0), (1, 5), (1, 6), (1, 11), (1, 12), (1, 17), (1, 18), (1, 19),
            (2, 1), (2, 4), (2, 7), (2, 10), (2, 13), (2, 16),
        ]

        for x, y in monster_shape:
            if lines[x][y] != '#':
                return False
        return True
