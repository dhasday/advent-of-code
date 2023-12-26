import networkx as nx

from aoc.common.day_solver import DaySolver


class Day25Solver(DaySolver):
    year = 2023
    day = 25

    def solve_puzzle_one(self):
        lines = self.load_all_input_lines()

        # TODO: Write code to do this faster
        graph = nx.Graph()
        for line in lines:
            wire, rest = line.split(': ')

            for w2 in rest.split(' '):
                graph.add_edge(wire, w2)
        cv, p = nx.stoer_wagner(graph)
        assert cv == 3
        return len(p[0]) * len(p[1])

    def solve_puzzle_two(self):
        return 'ALL DONE!'
