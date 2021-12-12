from collections import defaultdict, deque

from aoc.common.day_solver import DaySolver


class Day12Solver(DaySolver):
    year = 2021
    day = 12

    def _load_input(self, filename=None):
        lines = self.load_all_input_lines(filename)

        connections = defaultdict(lambda: [])
        can_revisit = set()
        for line in lines:
            node_1, node_2 = line.split('-')
            if node_1.isupper():
                can_revisit.add(node_1)
            if node_2.isupper():
                can_revisit.add(node_2)
            connections[node_1].append(node_2)
            connections[node_2].append(node_1)

        return connections, can_revisit

    def solve_puzzle_one(self):
        connections, can_revisit = self._load_input()

        all_paths = self._find_all_paths(connections, can_revisit, 'start', 'end')

        return len(all_paths)

    def solve_puzzle_two(self):
        connections, can_revisit = self._load_input()

        all_paths = self._find_all_paths_with_repeat(connections, can_revisit, 'start', 'end')

        return len(all_paths)

    def _find_all_paths(self, connections, can_revisit, start, end, visited=None):
        if visited is None:
            visited = set()

        visited.add(start)
        all_paths = []
        for adj in connections[start]:
            if adj == end:
                all_paths.append([start, end])
            elif adj in can_revisit or adj not in visited:
                adj_paths = self._find_all_paths(connections, can_revisit, adj, end, visited.copy())
                for path in adj_paths:
                    new_path = [start]
                    new_path.extend(path)
                    all_paths.append(new_path)

        return all_paths

    def _find_all_paths_with_repeat(self, connections, can_revisit, start, end, visited=None, has_repeat=False):
        if visited is None:
            visited = set()

        if start not in can_revisit:
            visited.add(start)
        all_paths = []
        for adj in connections[start]:
            if adj == end:
                all_paths.append([start, end])
                continue

            else:
                if adj not in visited:
                    adj_paths = self._find_all_paths_with_repeat(
                        connections,
                        can_revisit,
                        adj,
                        end,
                        visited.copy(),
                        has_repeat,
                    )
                elif not has_repeat and adj not in ('start', 'end'):
                    adj_paths = self._find_all_paths_with_repeat(
                        connections,
                        can_revisit,
                        adj,
                        end,
                        visited.copy(),
                        has_repeat=True,
                    )
                else:
                    adj_paths = []

                for path in adj_paths:
                    new_path = [start]
                    new_path.extend(path)
                    all_paths.append(new_path)

        return all_paths
