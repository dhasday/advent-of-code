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


class Day20Solver(DaySolver):
    year = 2020
    day = 20

    def solve_puzzle_one(self):
        all_tiles = self._load_tiles()

        all_tile_edges = self._get_tile_edges(all_tiles)
        corner_tiles, _ = self._find_edge_tiles(all_tile_edges)

        return functools.reduce(operator.mul, corner_tiles, 1)

    def solve_puzzle_two(self):
        return 'TODO'
        all_tiles = self._load_tiles()

        all_tile_edges = self._get_tile_edges(all_tiles)
        start_tile = next(iter(all_tile_edges))
        grid = self._find_grid_naive(all_tile_edges, start_tile)

        return 'TODO'

    def _load_tiles(self):
        all_tiles = {}

        cur_id = None
        cur_tile = set()
        cur_line = 0
        cur_edges = ['', '', '', '']
        for line in self.load_all_input_lines():
            if line.startswith('Tile'):
                cur_id = int(line[5:9])
            elif line == '':
                all_tiles[cur_id] = cur_tile, cur_edges
                cur_tile = set()
                cur_line = 0
                cur_edges = ['', '', '', '']
            else:
                if cur_line == 0:
                    cur_edges[0] = line
                if cur_line == TILE_SIZE - 1:
                    cur_edges[2] = line
                cur_edges[1] += line[TILE_SIZE - 1]
                cur_edges[3] += line[0]

                for idx, char in enumerate(line):
                    if char == '#':
                        cur_tile.add((idx, cur_line))
                cur_line += 1

        if cur_tile:
            all_tiles[cur_id] = cur_tile, cur_edges

        return all_tiles

    def _get_tile_edges(self, all_tiles):
        all_tile_edges = {}

        for tile, (_, edges) in all_tiles.items():
            # top, right, bottom, left -> top, left, bottom, right ?
            reversed_edges = [
                edges[0][::-1],
                edges[3][::-1],
                edges[2][::-1],
                edges[1][::-1],
            ]
            all_tile_edges[tile] = (edges, reversed_edges)

        return all_tile_edges

    def _find_edge_tiles(self, all_tile_edges):
        unique_edges = defaultdict(lambda: 0)
        for edges, reversed_edges in all_tile_edges.values():
            for e in edges:
                unique_edges[e] += 1
            for e in reversed_edges:
                unique_edges[e] += 1

        edge_patterns = {u for u in unique_edges if unique_edges[u] == 1}
        corner_tiles = set()
        edge_tiles = set()

        for tile, (edges, reversed_edges) in all_tile_edges.items():
            unmatched_edge_count = 0
            for e in edges:
                if e in edge_patterns:
                    unmatched_edge_count += 1
            for e in reversed_edges:
                if e in edge_patterns:
                    unmatched_edge_count += 1
            if unmatched_edge_count == 2:
                edge_tiles.add(tile)
            if unmatched_edge_count == 4:
                corner_tiles.add(tile)

        return corner_tiles, edge_tiles

    def _find_grid_naive(self, all_tile_edges, start_tile):
        def add_tile(_x, _y, _tile, _rotation, _flipped):
            grid[_x, _y] = _tile, _rotation, _flipped
            used_tiles[_tile] = _x, _y
            if _tile not in checked:
                to_check.add((_tile, _rotation, _flipped))

        grid = {
            (0, 0): (start_tile, 0, False),
        }

        used_tiles = dict()
        used_tiles[start_tile] = (0, 0)

        to_check = set()
        to_check.add((start_tile, 0, False))

        checked = set()

        while to_check:
            cur_tile, rotation, flipped = to_check.pop()
            x, y = used_tiles.get(cur_tile)

            match_above = self._get_edge_to_match(all_tile_edges, cur_tile, rotation, flipped, edge=0)  # (+0, +1), vs bottom other
            match_right = self._get_edge_to_match(all_tile_edges, cur_tile, rotation, flipped, edge=1)  # (+1, +0), vs left other
            match_below = self._get_edge_to_match(all_tile_edges, cur_tile, rotation, flipped, edge=2)  # (+0, -1), vs top other
            match_left = self._get_edge_to_match(all_tile_edges, cur_tile, rotation, flipped, edge=3)   # (-1, +0), vs right other

            for next_tile in all_tile_edges:
                if next_tile in used_tiles:
                    continue

                if (x - 1, y) not in grid:
                    rotation, flipped = self._get_match(all_tile_edges, next_tile, match_left)
                    if rotation:
                        add_tile(x - 1, y, next_tile, (rotation + 3) % 4, flipped)
                        continue

                if (x + 1, y) not in grid:
                    rotation, flipped = self._get_match(all_tile_edges, next_tile, match_right)
                    if rotation:
                        add_tile(x + 1, y, next_tile, (rotation + 1) % 4, flipped)
                        continue

                if (x, y - 1) not in grid:
                    rotation, flipped = self._get_match(all_tile_edges, next_tile, match_below)
                    if rotation:
                        add_tile(x, y - 1, next_tile, (rotation + 0) % 4, flipped)
                        continue

                if (x, y + 1) not in grid:
                    rotation, flipped = self._get_match(all_tile_edges, next_tile, match_above)
                    if rotation:
                        add_tile(x, y + 1, next_tile, (rotation + 2) % 4, flipped)
                        continue

        from ipdb import set_trace as bp
        bp()
        return grid

    def _get_match(self, all_tile_edges, tile, edge_to_match):
        for idx, edge in enumerate(all_tile_edges[tile][0]):
            if edge_to_match == edge:
                return idx, False
        for idx, edge in enumerate(all_tile_edges[tile][1]):
            if edge_to_match == edge:
                return idx, True
        return None, None

    def _match_adjacent(self, all_tile_edges, used_tiles, cur_tile):
        pass

    def _get_edge_to_match(self, all_tile_edges, tile, rotation, flipped, edge=0):
        return all_tile_edges[tile][1 if flipped else 0][(rotation + edge) % 4]

    # def _find_grid(self, all_tile_edges, start_tile):
    #     edge_counts = defaultdict(lambda: 0)
    #     for edges, reversed_edges in all_tile_edges.values():
    #         for e in edges:
    #             edge_counts[e] += 1
    #         for e in reversed_edges:
    #             edge_counts[e] += 1
    #
    #     start_orientations = self._get_valid_corner_orientations(all_tile_edges[start_tile], edge_counts)
    #
    #     for rotation, flipped in start_orientations:
    #         grid, is_complete = self._try_build_grid(all_tile_edges, start_tile, rotation, flipped)
    #         if is_complete:
    #             return grid
    #
    #     raise Exception('Well that didn\'t work')
    #
    # def _get_valid_corner_orientations(self, tile, edge_counts):
    #     def get_orientation(edges):
    #         unmatched_edges = []
    #         for i, e in enumerate(edges):
    #             if edge_counts[e] == 1:
    #                 unmatched_edges.append(i)
    #         if unmatched_edges[0] + 1 == unmatched_edges[1]:
    #             return unmatched_edges[1]
    #         else:
    #             return unmatched_edges[0]
    #
    #     return [
    #         (get_orientation(tile[0]), False),
    #         (get_orientation(tile[1]), True),
    #     ]
    #
    # def _build_grid(self, all_tile_edges, corner_tiles):
    #     grid = self._build_outer_edge(all_tile_edges, corner_tiles)
    #
    #     return grid
    #
    # def _build_outer_edge(self, all_tile_edges, corner_tiles):
    #     def _find_match(_grid, _used_tiles, _to_match, offset, target_x, target_y):
    #         for possible_tile in all_tile_edges:
    #             if possible_tile not in _used_tiles:
    #                 match_rotation, match_flipped = _get_match(possible_tile, _to_match)
    #                 if match_rotation is not None:
    #                     _grid[target_x, target_y] = possible_tile, (match_rotation + offset) % 4, match_flipped
    #                     _used_tiles.add(possible_tile)
    #                     return True
    #         return False
    #
    #     def _get_match(tile, edge_to_match):
    #         for idx, edge in enumerate(all_tile_edges[tile][0]):
    #             if edge_to_match == edge:
    #                 return idx, False
    #         for idx, edge in enumerate(all_tile_edges[tile][1]):
    #             if edge_to_match == edge:
    #                 return idx, True
    #         return None, None
    #
    #     edge_counts = defaultdict(lambda: 0)
    #     for edges, reversed_edges in all_tile_edges.values():
    #         for e in edges:
    #             edge_counts[e] += 1
    #         for e in reversed_edges:
    #             edge_counts[e] += 1
    #
    #
    #     print({
    #         'e1': sum(1 for e in edge_counts.items() if e[1] == 1),
    #         'e2': sum(1 for e in edge_counts.items() if e[1] == 2),
    #         'e+': sum(1 for e in edge_counts.items() if e[1] > 2),
    #     })
    #
    #     start_tile = next(iter(corner_tiles))  # Pick a random corner to start with
    #     start_orientations = self._get_valid_corner_orientations(all_tile_edges[start_tile], edge_counts)
    #
    #     # Use a random orientation and we'll fix later since there should be 2 solutions (original/flipped)
    #     grid = {
    #         (0, 0): (start_tile, start_orientations[0][0] + 1 % 4, start_orientations[0][1]),
    #     }
    #
    #     used_tiles = {start_tile}
    #
    #     # Do one side first (bottom edge)
    #     for y in range(1, GRID_SIZE):
    #         to_match = self._get_edge_to_match(all_tile_edges, grid[0, y - 1], edge=1)
    #         found = _find_match(grid, used_tiles, to_match, 1, 0, y)
    #         if not found:
    #             raise Exception('oops')
    #
    #     # 0, 0
    #
    #     # 0 ... 12
    #     #
    #     # Build from that side
    #     for x in range(1, GRID_SIZE):
    #         for y in range(0, GRID_SIZE):
    #             print(x, y, len(grid))
    #             from ipdb import set_trace as bp
    #             bp()
    #             to_match = self._get_edge_to_match(all_tile_edges, grid[x - 1, y], edge=0)
    #             found = _find_match(grid, used_tiles, to_match, 2, x, y)
    #             if not found:
    #                 raise Exception('oops')
    #
    #     from ipdb import set_trace as bp
    #     bp()
    #     return grid
    #
    # def _try_build_grid(self, all_tile_edges, start_tile, rotation, flipped):
    #     grid = {
    #         (0, 0): (start_tile, rotation, flipped),
    #     }
    #
    #     used_tiles = set()
    #     used_tiles.add(start_tile)
    #
    #     for x in range(TILE_SIZE):
    #         if x > 0:  # Only need to match the bottom to next top after the first row
    #             tile_above = grid[(0, x - 1)] if x > 0 else None
    #             above_options = self._find_next_tile(
    #                 all_tile_edges,
    #                 used_tiles,
    #                 above=self._get_edge_to_match(all_tile_edges, tile_above, edge=0),
    #             )
    #         else:
    #             above_options = [None]
    #
    #         for above_option in above_options:
    #             for y in range(1, TILE_SIZE):
    #                 tile_above = grid[(x - 1, y)] if x > 0 else None
    #                 tile_left = grid[(x, y - 1)]
    #
    #                 right_options = self._find_next_tile(
    #                     all_tile_edges,
    #                     used_tiles,
    #                     above=self._get_edge_to_match(all_tile_edges, tile_above, edge=0),
    #                     left=self._get_edge_to_match(all_tile_edges, tile_left, edge=1),
    #                 )
    #                 if not right_options:
    #                     continue
    #
    #     return grid, True
    #

    # def _find_next_tile(self, all_tile_edges, used_tiles, above=None, left=None, below=None, right=None):
    #     options = {}
    #     for tile, (edges, reversed_edges) in all_tile_edges.items():
    #         top_edge = None, None
    #         for idx, edge in enumerate(edges):
    #             if edge
    #         if above and left:
    #             pass
    #         elif above:
    #             pass
    #         elif left:
    #             pass
    #
    #     return None, None, None
