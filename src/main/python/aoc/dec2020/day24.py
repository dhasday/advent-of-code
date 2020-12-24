from aoc.common.day_solver import DaySolver
from aoc.common.helpers import HEX_DIRECTION_OFFSETS


class Day24Solver(DaySolver):
    year = 2020
    day = 24

    def solve_puzzles(self):
        all_directions = self._load_input()

        flipped_tiles = set()
        for directions in all_directions:
            dest = self._get_destination(directions, (0, 0, 0))
            if dest in flipped_tiles:
                flipped_tiles.remove(dest)
            else:
                flipped_tiles.add(dest)
        ans_one = len(flipped_tiles)

        for i in range(100):
            flipped_tiles = self._flip_tiles(flipped_tiles)
        ans_two = len(flipped_tiles)

        return ans_one, ans_two

    def _load_input(self):
        all_directions = []
        for line in self.load_all_input_lines():
            directions = []
            prev = ''
            for c in line:
                if prev in ['n', 's']:
                    directions.append(prev + c)
                elif c not in ['n', 's']:
                    directions.append(c)
                prev = c
            all_directions.append(directions)

        return all_directions

    def _get_destination(self, directions, start):
        cur = start

        for direction in directions:
            cur = HEX_DIRECTION_OFFSETS[direction](cur)
        return cur

    def _flip_tiles(self, flipped_tiles):
        checked = set()
        to_check = set(flipped_tiles)
        out = set()

        while to_check:
            cur_tile = to_check.pop()
            if cur_tile in checked:
                continue
            checked.add(cur_tile)

            adjacent_tiles = self._get_adjacent_tiles(cur_tile)
            neighbors = 0
            for tile in adjacent_tiles:
                if tile in flipped_tiles:
                    neighbors += 1

            if cur_tile in flipped_tiles:
                if 0 < neighbors <= 2:
                    out.add(cur_tile)
            elif neighbors == 2:
                out.add(cur_tile)

            if neighbors > 0:
                for tile in adjacent_tiles:
                    if tile not in checked:
                        to_check.add(tile)

        return out

    def _get_adjacent_tiles(self, cur_tile):
        neighbors = set()
        for offset in HEX_DIRECTION_OFFSETS.values():
            neighbors.add(offset(cur_tile))
        return neighbors
