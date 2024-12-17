import heapq

from aoc.common import helpers
from aoc.common.day_solver import DaySolver


class Day16Solver(DaySolver):
    year = 2024
    day = 16

    END_DIR = 0, 0

    def solve_puzzles(self):
        maze, start_pos, end_pos = self.load_input()

        start_dir = 1, 0

        mapped_maze = self.map_maze(maze, start_pos, start_dir, end_pos)

        lowest_score, _ = mapped_maze.get((end_pos, self.END_DIR))

        viewing_spots = self.count_viewing_spots(mapped_maze, end_pos)

        return lowest_score, viewing_spots

    def load_input(self):
        lines = self.load_all_input_lines()

        maze = set()
        start_pos = None
        end_pos = None

        for y, line in enumerate(lines):
            for x, val in enumerate(line):
                pos = x, y
                if val == '.':
                    maze.add(pos)
                elif val == 'S':
                    maze.add(pos)
                    start_pos = pos
                elif val == 'E':
                    maze.add(pos)
                    end_pos = pos

        return maze, start_pos, end_pos

    def map_maze(self, maze, start_pos, start_dir, end_pos):
        open_set = []
        closed_set = dict()

        heapq.heappush(open_set, (0, start_pos, start_dir))
        closed_set[start_pos, start_dir] = (0, [])

        while open_set:
            cur_score, cur_pos, cur_dir = heapq.heappop(open_set)

            cur_node = closed_set.get((cur_pos, cur_dir))
            if cur_node[0] < cur_score:
                continue

            for (adj_pos, adj_dir, adj_score) in self._get_adj_nodes(maze, cur_pos, cur_dir):
                if adj_pos == end_pos:
                    adj_dir = self.END_DIR

                adj_node = closed_set.get((adj_pos, adj_dir))
                new_score = cur_score + adj_score

                if not adj_node or new_score < adj_node[0]:
                    closed_set[adj_pos, adj_dir] = (new_score, [(cur_pos, cur_dir)])
                    heapq.heappush(open_set, (new_score, adj_pos, adj_dir))
                elif new_score == adj_node[0]:
                    closed_set[adj_pos, adj_dir][1].append((cur_pos, cur_dir))

        return closed_set

    def count_viewing_spots(self, mapped_nodes, end_pos):
        to_check = {(end_pos, self.END_DIR)}

        seen = set()
        while to_check:
            cur_node = to_check.pop()
            seen.add(cur_node[0])
            to_check.update(v for v in mapped_nodes.get(cur_node)[1])

        return len(seen)

    def _get_adj_nodes(self, maze, cur_pos, cur_dir):
        adj_nodes = []

        forward_pos = helpers.apply_deltas(cur_pos, cur_dir)
        if forward_pos in maze:
            adj_nodes.append((forward_pos, cur_dir, 1))

        left_dir = -cur_dir[1], -cur_dir[0]
        left_pos = helpers.apply_deltas(cur_pos, left_dir)
        if left_pos in maze:
            adj_nodes.append((left_pos, left_dir, 1001))

        right_dir = cur_dir[1], cur_dir[0]
        right_pos = helpers.apply_deltas(cur_pos, right_dir)
        if right_pos in maze:
            adj_nodes.append((right_pos, right_dir, 1001))

        return adj_nodes
