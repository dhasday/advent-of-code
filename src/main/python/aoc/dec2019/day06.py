from aoc.common.day_solver import DaySolver
from aoc.common.dijkstra_search import DijkstraSearch


class Day06Solver(DaySolver):
    year = 2019
    day = 6

    def solve_puzzle_one(self):
        orbits = self._load_orbits(symmetric=False)

        return self._count_orbits(orbits, 'COM', 0)

    def solve_puzzle_two(self):
        orbits = self._load_orbits(symmetric=True)

        min_distance = self._find_min_distance(orbits, 'YOU', 'SAN')

        return min_distance - 2

    def _load_orbits(self, symmetric):
        lines = self.load_all_input_lines()

        orbits = dict()
        for line in lines:
            planets = line.split(')')
            inner = planets[0]
            outer = planets[1]

            if inner not in orbits:
                orbits[inner] = set()
            orbits[inner].add(outer)

            if symmetric:
                if outer not in orbits:
                    orbits[outer] = set()
                orbits[outer].add(inner)

        return orbits

    def _count_orbits(self, orbits, planet, distance):
        count = distance

        if planet in orbits:
            for p in orbits[planet]:
                count += self._count_orbits(orbits, p, distance + 1)

        return count

    def _find_min_distance(self, orbits, start, end):
        search = DijkstraSearch(lambda p: [(v, 1) for v in orbits[p]])
        path, distance = search.find_shortest_path(start, end)
        return distance
