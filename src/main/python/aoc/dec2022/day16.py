import re

from aoc.common.day_solver import DaySolver
from aoc.common.dijkstra_search import DijkstraSearch

INPUT_REGEX = re.compile(r'Valve ([A-Z][A-Z]) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z, ]+)')


class Valve(object):
    def __init__(self, name, rate, connections):
        self.name = name
        self.rate = rate
        self.connections = connections
        self.distances = None

    def calc_distances(self, all_valves):
        if self.distances is None:
            def find_adj(n):
                return [(all_valves[c], 1) for c in n.connections]

            search = DijkstraSearch(find_adj)
            results = search._execute_search(self)
            self.distances = {}
            for other_valve in all_valves.values():
                if other_valve.name == self.name:
                    continue

                if other_valve.rate != 0:
                    self.distances[other_valve] = results[other_valve].distance + 1

        return self.distances

    def total_flow(self, remaining_time):
        return self.rate * remaining_time

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self):
        return f'Valve({self.name})'


class Day16Solver(DaySolver):
    year = 2022
    day = 16

    flow_valves = None

    def setup(self):
        lines = self.load_all_input_lines()

        all_valves = {}
        self.flow_valves = {}
        for line in lines:
            result = INPUT_REGEX.findall(line)
            valve = result[0][0]
            flow_rate = int(result[0][1])
            connections = result[0][2].split(', ')

            all_valves[valve] = Valve(valve, flow_rate, connections)
            if flow_rate > 0 or valve == 'AA':
                self.flow_valves[valve] = Valve(valve, flow_rate, connections)

        for node in self.flow_valves.values():
            node.calc_distances(all_valves)

    def solve_puzzle_one(self):
        unvisited_valves = {v for v in self.flow_valves.values() if v.name != 'AA'}
        start_valve = self.flow_valves['AA']
        possible_orders = self._all_possible_orders(unvisited_valves, 30, start_valve, [])
        return max(self._get_result(start_valve, 30, order) for order in possible_orders)

    def solve_puzzle_two(self):
        unvisited_valves = {v for v in self.flow_valves.values() if v.name != 'AA'}
        start_valve = self.flow_valves['AA']
        possible_orders = self._all_possible_orders(unvisited_valves, 26, start_valve, [])

        results = [(self._get_result(start_valve, 26, order), set(order)) for order in possible_orders]
        results.sort(key=lambda x: -x[0])

        best = 0
        for idx, (score_1, order_1) in enumerate(results):
            if score_1 * 2 < best:
                break
            for score_2, order_2 in results[idx+1:]:
                if not order_1 & order_2:
                    best = max(best, score_1 + score_2)
        return best

    def _all_possible_orders(self, unvisited_valves, remaining_time, cur_value, cur_order):
        for next_valve in unvisited_valves:
            cost = cur_value.distances[next_valve]
            if cost < remaining_time:
                yield from self._all_possible_orders(
                    unvisited_valves - {next_valve},
                    remaining_time - cost,
                    next_valve,
                    cur_order + [next_valve],
                )
        yield cur_order

    def _get_result(self, start_valve, time, order):
        total = 0
        cur_valve = start_valve
        cur_time = time
        for valve in order:
            cur_time -= (cur_valve.distances[valve])
            total += valve.total_flow(cur_time)
            cur_valve = valve
        return total
