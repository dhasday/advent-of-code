from collections import deque

from aoc.common import helpers
from aoc.common.day_solver import DaySolver


max_remaining_geodes = {1: 0}
for i in range(2, 33):
    max_remaining_geodes[i] = max_remaining_geodes[i - 1] + i - 1


class Blueprint(object):
    def __init__(self, line):
        values = [int(v) for v in helpers.ALL_NUMBERS_REGEX.findall(line)]
        self.id = values[0]

        self.ore_cost = values[1]  # Ore
        self.clay_cost = values[2]  # Ore
        self.obsidian_cost = values[3], values[4]  # Ore, Clay
        self.geode_cost = values[5], values[6]  # Ore, Obsidian

        self.max_ore = max(self.ore_cost, self.clay_cost, self.obsidian_cost[0], self.geode_cost[0])
        self.max_clay = self.obsidian_cost[1]
        self.max_obsidian = self.geode_cost[1]

    def get_max_geodes(self, time):
        # print(f'{self.id}: ore({self.ore_cost}), clay({self.clay_cost}), obsidian{self.obsidian_cost}, geode{self.geode_cost}')
        # Robot Count - Resources
        start_state = (1, 0, 0, 0, 0, 0, 0, time)

        open_states = deque([start_state])
        closed_states = set()
        max_geodes = 0
        while open_states:
            cur_state = open_states.popleft()
            ore_bot, clay_bot, obsidian_bot, ore, clay, obsidian, geode, time = cur_state

            if geode > max_geodes:
                max_geodes = geode

            if time == 1:
                continue

            # Simplify state to decrease checks
            # If we can't use all the ore, then simplify state
            ore = min(ore, self.max_ore * time)
            clay = min(clay, self.max_clay * time)
            obsidian = min(obsidian, self.max_obsidian * time)

            # We only need at most enough robots to replenish the max resource amount consumed on a given round
            # ore_bot = min(ore_bot, self.max_ore)
            # clay_bot = min(clay_bot, self.max_clay)
            # obsidian_bot = min(obsidian_bot, self.max_obsidian)

            cur_state = ore_bot, clay_bot, obsidian_bot, ore, clay, obsidian, geode, time
            if cur_state in closed_states:
                continue
            closed_states.add(cur_state)

            # if we can't create enough geodes to set a new record, don't process
            if max_geodes > geode + max_remaining_geodes[time]:
                continue

            if ore >= self.geode_cost[0] and obsidian >= self.geode_cost[1]:
                open_states.append((
                    ore_bot, clay_bot, obsidian_bot,
                    ore - self.geode_cost[0] + ore_bot, clay + clay_bot, obsidian - self.geode_cost[1] + obsidian_bot, geode + time - 1,
                    time - 1
                ))

            if obsidian_bot < self.max_obsidian and ore >= self.obsidian_cost[0] and clay >= self.obsidian_cost[1]:
                open_states.append((
                    ore_bot, clay_bot, obsidian_bot + 1,
                    ore - self.obsidian_cost[0] + ore_bot, clay - self.obsidian_cost[1] + clay_bot, obsidian + obsidian_bot, geode,
                    time - 1
                ))

            if clay_bot < self.max_clay and ore >= self.clay_cost:
                open_states.append((
                    ore_bot, clay_bot + 1, obsidian_bot,
                    ore - self.clay_cost + ore_bot, clay + clay_bot, obsidian + obsidian_bot, geode,
                    time - 1
                ))

            if ore_bot < self.max_ore and ore >= self.ore_cost:
                open_states.append((
                    ore_bot + 1, clay_bot, obsidian_bot,
                    ore - self.ore_cost + ore_bot, clay + clay_bot, obsidian + obsidian_bot, geode,
                    time - 1
                ))

            open_states.append((
                ore_bot, clay_bot, obsidian_bot,
                ore + ore_bot, clay + clay_bot, obsidian + obsidian_bot, geode,
                time - 1
            ))

        # print(f'\t{max_geodes}')
        return max_geodes


class Day19Solver(DaySolver):
    year = 2022
    day = 19

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        blueprints = []
        for line in lines:
            blueprints.append(Blueprint(line))

        p1 = sum(b.id * b.get_max_geodes(24) for b in blueprints)

        p2 = 1
        for blueprint in blueprints[:3]:
            p2 *= blueprint.get_max_geodes(32)

        return p1, p2


Day19Solver().print_results()
