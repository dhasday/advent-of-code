import functools
import operator
from collections import defaultdict

from aoc.common.day_solver import DaySolver


TILE_SIZE = 10
GRID_SIZE = 12

# Rotate
# XXXX. > X.X.X > ....X > ..X..     | XXXX. ..X.. ....X X.X.X
# .XXX. > .X.XX > .X.X. > XX.X.     | X.X.X XXXX. ..X.. ....X
# X...X > ...XX > X...X > XX...     | ....X X.X.X XXXX. ..X..
# .X.X. > .X.XX > .XXX. > XX.X.     | ..X.. ....X X.X.X XXXX.
# X.... > ..X.. > .XXXX > X.X.X

# Fliped
# X.... > X.X.X > .XXXX > ..X..     | X.... ..X.. .XXXX X.X.X
# .X.X. > XX.X. > .XXX. > .X.XX     | X.X.X X.... ..X.. .XXXX
# X...X > XX... > X...X > ...XX     | .XXXX X.X.X X.... ..X..
# .XXX. > XX.X. > .X.X. > .X.XX     | ..X.. .XXXX X.X.X X....
# XXXX. > ..X.. > ....X > X.X.X

# 2657
#   #.##..##..
#   ....#.#...
#   #...#.....
#   ..##..####
#   .#.......#
#   ##......##
#   ..#.#.#..#
#   ...#.....#
#   #..#......
#   #.##..#...

# 1609
#   ##..##.##.
#   .#.#...##.
#   #........#
#   #....#...#
#   .#......##
#   ..#......#
#   #...#.....
#   .#........
#   ...#.....#
#   ..#.###...

SIDE_TOP = 0
SIDE_RIGHT = 1
SIDE_BOTTOM = 2
SIDE_LEFT = 3


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
            return self.__class__(self.id, list(zip(*self.lines[::-1])))

        def flip(self):
            return self.__class__(self.id, [i[::-1] for i in self.lines])

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

        from ipdb import set_trace as bp
        bp()
        start_tile = next(iter(all_tiles.values()))
        grid = self._find_grid(all_tiles, start_tile)

        # TODO: Convert grid into resulting picture
        #       Scan for shape and count others in all rotations and flipped
        #       Return count others when most found shape

        return 'TODO'

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
                cur_tile.append(line)

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
        grid = {
            (0, 0): start_tile,
        }

        placed_tiles = {
            start_tile: (0, 0),
        }

        to_check = set()
        to_check.add(start_tile)

        while to_check:
            cur_tile = to_check.pop()
            cur_x, cur_y = placed_tiles.get(cur_tile)

            for next_tile in all_tiles.values():
                if next_tile in placed_tiles:
                    continue

                if cur_tile.get_side(SIDE_TOP) in next_tile.edges:
                    rotated_tile = self._fix_orientation(next_tile, SIDE_BOTTOM, cur_tile.get_side(SIDE_TOP))
                    next_pos = cur_x, cur_y - 1
                    grid[next_pos] = rotated_tile
                    placed_tiles[rotated_tile] = next_pos
                    to_check.add(rotated_tile)
                elif cur_tile.get_side(SIDE_BOTTOM) in next_tile.edges:
                    rotated_tile = self._fix_orientation(next_tile, SIDE_TOP, cur_tile.get_side(SIDE_BOTTOM))
                    next_pos = cur_x, cur_y + 1
                    grid[next_pos] = rotated_tile
                    placed_tiles[rotated_tile] = next_pos
                    to_check.add(rotated_tile)
                elif cur_tile.get_side(SIDE_LEFT) in next_tile.edges:
                    rotated_tile = self._fix_orientation(next_tile, SIDE_RIGHT, cur_tile.get_side(SIDE_LEFT))
                    next_pos = cur_x - 1, cur_y
                    grid[next_pos] = rotated_tile
                    placed_tiles[rotated_tile] = next_pos
                    to_check.add(rotated_tile)
                elif cur_tile.get_side(SIDE_RIGHT) in next_tile.edges:
                    rotated_tile = self._fix_orientation(next_tile, SIDE_LEFT, cur_tile.get_side(SIDE_RIGHT))
                    next_pos = cur_x + 1, cur_y
                    grid[next_pos] = rotated_tile
                    placed_tiles[rotated_tile] = next_pos
                    to_check.add(rotated_tile)

        return grid

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
