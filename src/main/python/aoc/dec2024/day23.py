from collections import defaultdict

from aoc.common.day_solver import DaySolver


class Day23Solver(DaySolver):
    year = 2024
    day = 23

    connections = None

    def solve_puzzles(self):
        lines = self.load_all_input_lines()
        self.connections = defaultdict(set)
        for line in lines:
            a, b = line.split('-')
            self.connections[a].add(b)
            self.connections[b].add(a)

        valid_triples = set()
        for host in self.connections:
            for t_1 in self.connections[host]:
                for t_2 in self.connections[host]:
                    if self._is_valid_triple(host, t_1, t_2):
                        valid_triples.add(tuple(sorted([host, t_1, t_2])))

        # Added a short circuit where we stop looking if we find the max possible network size
        max_size = max(len(n) for n in self.connections.values())
        initial_p = set(self.connections.keys())
        max_result = self._bron_kerbosch(set(), initial_p, set(), max_size)

        return len(valid_triples), ','.join(sorted(max_result))

    def _is_valid_triple(self, a, b, c):
        if b == c:
            return False

        if a[0] != 't' and b[0] != 't' and c[0] != 't':
            return False

        if b not in self.connections[c]:
            return False

        if c not in self.connections[b]:
            return False

        return True

    def _bron_kerbosch(self, r: set, p: set, x: set, max_size):
        # https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm
        if not p and not x:
            return set(r)

        max_result = set()

        for v in set(p):
            next_r = set(r)
            next_r.add(v)
            next_p = p.intersection(self.connections[v])
            next_x = x.intersection(self.connections[v])

            cur_result = self._bron_kerbosch(next_r, next_p, next_x, max_size)
            if len(cur_result) > len(max_result):
                if len(cur_result) == max_size:
                    return cur_result
                max_result = cur_result

            p.remove(v)
            x.add(v)

        return max_result


for _ in range(10):
    Day23Solver().print_results()