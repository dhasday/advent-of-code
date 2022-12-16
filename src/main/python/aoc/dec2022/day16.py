import re

from aoc.common.day_solver import DaySolver
from aoc.common.dijkstra_search import DijkstraSearch

INPUT_REGEX = re.compile(r'Valve ([A-Z][A-Z]) has flow rate=(\d+); tunnels? leads? to valves? ([A-Z, ]+)')


class Day16Solver(DaySolver):
    year = 2022
    day = 16

    memo = None

    def setup(self):
        # lines = self.load_all_input_lines(example=True)
        lines = self.load_all_input_lines()

        self.connections = {}
        self.flow_rates = {}
        for line in lines:
            result = INPUT_REGEX.findall(line)
            valve = result[0][0]
            flow_rate = int(result[0][1])
            cur_connections = result[0][2].split(', ')

            self.connections[valve] = cur_connections
            if flow_rate != 0:
                self.flow_rates[valve] = flow_rate

        def find_adj(cur_valve):
            return [(c, 1) for c in self.connections[cur_valve]]

        search = DijkstraSearch(find_adj)
        self.distances = {}
        for valve in self.connections:
            results = search._execute_search(valve)
            self.distances[valve] = {}
            for v in self.flow_rates.keys():
                self.distances[valve][v] = results[v].build_path()[1:]

    def solve_puzzle_one(self):
        self.memo = {}
        closed_valves = set(self.flow_rates.keys())
        return self._get_max_release('AA', closed_valves, 30)

    def solve_puzzle_two(self):
        return 2400
        self.memo = {}
        closed_valves = set(self.flow_rates.keys())
        return self._get_max_release_two('AA', 'AA', closed_valves, 26)

    def _get_max_release(self, cur_valve, closed_valves, remaining_time):
        state = f'{remaining_time} {cur_valve} {sorted(closed_valves)}'
        if state in self.memo:
            return self.memo[state]

        if remaining_time < 1:
            return 0

        current_flow = sum(v for k, v in self.flow_rates.items() if k not in closed_valves)
        if remaining_time == 1:
            self.memo[state] = current_flow
            return current_flow

        if len(closed_valves) == 0:
            result = current_flow + self._get_max_release('XX', closed_valves, remaining_time - 1)
            self.memo[state] = result
            return result

        max_total = 0

        for next_valve in closed_valves:
                advance_by = len(self.distances[cur_valve][next_valve]) + 1
                next_closed_valves = closed_valves.difference({next_valve})

                if advance_by >= remaining_time:
                    advance_by = remaining_time
                    new_total = 0
                else:
                    new_total = self._get_max_release(next_valve, next_closed_valves, remaining_time - advance_by)

                new_total += current_flow * (advance_by - 1)
                max_total = max(max_total, new_total)

        result = max_total + current_flow
        self.memo[state] = result
        return result

    def _get_max_release_two(self, cur_valve_1, cur_valve_2, closed_valves, remaining_time):
        state = f'{remaining_time} {sorted([cur_valve_1, cur_valve_2])} {sorted(closed_valves)}'
        if state in self.memo:
            return self.memo[state]

        if remaining_time < 1:
            return 0

        current_flow = sum(v for k, v in self.flow_rates.items() if k not in closed_valves)
        if remaining_time == 1:
            self.memo[state] = current_flow
            return current_flow

        if len(closed_valves) == 0:
            result = current_flow + self._get_max_release_two('XX', 'XX', closed_valves, remaining_time - 1)
            self.memo[state] = result
            return result

        max_total = 0

        for action_1 in closed_valves:
            for action_2 in closed_valves:
                if action_1 == action_2 and len(closed_valves) > 1:
                    continue

                time_1 = len(self.distances[cur_valve_1][action_1]) + 1
                time_2 = len(self.distances[cur_valve_2][action_2]) + 1

                advance_by = min(time_1, time_2)
                next_closed_valves = closed_valves.copy()

                if time_1 > advance_by:
                    next_valve_1 = self.distances[cur_valve_1][action_1][advance_by - 1]
                else:
                    next_valve_1 = action_1
                    next_closed_valves.discard(action_1)

                if time_2 > advance_by:
                    next_valve_2 = self.distances[cur_valve_2][action_2][advance_by - 1]
                else:
                    next_valve_2 = action_2
                    next_closed_valves.discard(action_2)

                if advance_by >= remaining_time:
                    advance_by = remaining_time
                    new_total = 0
                else:
                    new_total = self._get_max_release_two(next_valve_1, next_valve_2, next_closed_valves, remaining_time - advance_by)
                new_total += current_flow * (advance_by - 1)
                max_total = max(max_total, new_total)

        result = max_total + current_flow
        self.memo[state] = result
        return result


Day16Solver().print_results()
