from enum import Enum

from aoc.common.breadth_first_search import BreadthFirstSearch
from aoc.common.day_solver import DaySolver

HP_START = 200

DIR_UP = 'UP'
DIR_DOWN = 'DOWN'
DIR_LEFT = 'LEFT'
DIR_RIGHT = 'RIGHT'
ORDERED_DIRECTIONS = [DIR_LEFT, DIR_UP, DIR_DOWN, DIR_RIGHT]
POS_OFFSET = {
    DIR_UP: (0, -1),
    DIR_DOWN: (0, 1),
    DIR_LEFT: (-1, 0),
    DIR_RIGHT: (1, 0),
}


class Day15Solver(DaySolver):
    year = 2018
    day = 15

    class UnitType(Enum):
        ELF = 'E'
        GOBLIN = 'G'

    class Unit(object):
        def __init__(self, pos, value=None, type=None, power=3):
            self.pos = pos
            self.hp = 200

            self.type = type if type else Day15Solver.UnitType(value)
            self.power = power

        @property
        def alive(self):
            return self.hp > 0

        def __str__(self):
            return '{}: {} {} HP'.format(self.type, self.pos, self.hp)

        def move(self, barriers, enemy_positions):
            bfs = Day15Solver.EnemyBFS(self.pos, barriers, enemy_positions)

            if self.pos in bfs.targets:
                return False

            next_pos = bfs.find_next_position()

            if next_pos is None:
                return False
            else:
                self.pos = next_pos
                return True

        def attack(self, units):
            neighbors = [(self.pos[0] + POS_OFFSET[o][0], self.pos[1] + POS_OFFSET[o][1]) for o in ORDERED_DIRECTIONS]

            # Find all adjacent enemies
            adj_enemies = [None, None, None, None]
            for enemy in units:
                if enemy.type == self.type or not enemy.alive:
                    continue

                if enemy.pos in neighbors:
                    adj_enemies[neighbors.index(enemy.pos)] = enemy

            # Determine which adjacent enemy to target
            target = None
            for e in adj_enemies:
                if e is not None:
                    if target is None or e.hp < target.hp:
                        target = e

            if target is not None:
                target.hp -= self.power

            return target

    class EnemyBFS(BreadthFirstSearch):
        def __init__(self, start, barriers, enemy_positions):
            self.start = start
            self.barriers = barriers

            self.targets = []
            for pos in enemy_positions:
                for offset in POS_OFFSET.values():
                    target_pos = (pos[0] + offset[0], pos[1] + offset[1])
                    self.targets.append(target_pos)

        def find_next_position(self):
            shortest_path = self.find_path_multiple_targets(self.start, self.targets, self._adjacent_positions)

            if shortest_path is None or len(shortest_path) < 2:
                return None

            return shortest_path[1]

        def _adjacent_positions(self, pos):
            adj_positions = []

            for d in ORDERED_DIRECTIONS:
                offset = POS_OFFSET[d]
                next_pos = pos[0] + offset[0], pos[1] + offset[1]
                if next_pos not in self.barriers:
                    adj_positions.append(next_pos)

            return adj_positions

    def solve_puzzle_one(self):
        walls, units, size = self._load_input()

        return self._run_simulation(walls, units, size)

    def solve_puzzle_two(self):
        walls, units, size = self._load_input()

        elf_count, goblin_count = self._count_units(units)

        # 200 is starting HP, so powering up the elves more is clearly overkill
        for i in range(4, 200):
            units_copy = []
            for u in units:
                power = i if u.type == Day15Solver.UnitType.ELF else 3
                units_copy.append(self.Unit(u.pos, type=u.type, power=power))

            result = self._run_simulation(walls, units_copy, size, break_on_elf_death=True)

            remaining_elves, _ = self._count_units(units_copy)

            if remaining_elves == elf_count:
                return result

        return 'ERROR'

    def _load_input(self, filename=None):
        walls = set()
        units = list()

        size = 0

        for x, row in enumerate(self._load_all_input_lines(filename=filename)):
            for y, value in enumerate(row):
                pos = (x, y)

                if value == '#':
                    walls.add(pos)
                elif value in ['E', 'G']:
                    units.append(self.Unit(pos, value))

                size = max(size, x, y)

        return walls, units, size + 1

    def _run_simulation(self, walls, units, size, break_on_elf_death=False, debug=False):
        if debug:
            self._print_board(size, walls, units)

        rounds = 0
        num_elves, num_goblins = self._count_units(units)
        units = self._sort_and_remove_dead_units(units)
        round_complete = True
        while num_elves and num_goblins:
            round_complete = True
            for unit in units:
                if not unit.alive:
                    continue

                barriers = self._get_barriers(walls, units)
                enemy_positions = self._get_enemy_positions(unit, units)

                if len(enemy_positions) == 0:
                    round_complete = False
                    continue

                unit.move(barriers, enemy_positions)
                target = unit.attack(units)

                if break_on_elf_death \
                        and target \
                        and target.type == self.UnitType.ELF \
                        and not target.alive:
                    return None

            num_elves, num_goblins = self._count_units(units)
            units = self._sort_and_remove_dead_units(units)

            rounds += 1
            if debug:
                self._print_board(size, walls, units, rounds)

        remaining_hp = 0
        for u in units:
            if u.alive:
                remaining_hp += u.hp

        if not round_complete:
            rounds -= 1
        return rounds * remaining_hp

    def _count_units(self, units):
        counts = {}

        for u in units:
            if u.hp > 0:
                if u.type not in counts:
                    counts[u.type] = 1
                else:
                    counts[u.type] += 1

        return counts.get(self.UnitType.ELF), counts.get(self.UnitType.GOBLIN)

    def _sort_and_remove_dead_units(self, units):
        remaining_units = filter(lambda u1: u1.hp > 0, units)
        return sorted(remaining_units, key=lambda u2: u2.pos)

    def _get_barriers(self, walls, units):
        barriers = walls.copy()
        for u in units:
            if u.alive:
                barriers.add(u.pos)
        return barriers

    def _get_enemy_positions(self, unit, units):
        enemy_positions = []
        for u in units:
            if u.type != unit.type and u.alive:
                enemy_positions.append(u.pos)
        return enemy_positions

    def _print_board(self, size, walls, units, rounds=0):
        board = [['.'] * size for _ in range(size)]

        for w in walls:
            board[w[0]][w[1]] = '#'

        for u in units:
            unit_char = 'E' if u.type == Day15Solver.UnitType.ELF else 'G'
            board[u.pos[0]][u.pos[1]] = unit_char

        print 'Round {}'.format(rounds)
        for row in board:
            line = ''
            for col in row:
                line += col
            print line
        for u in units:
            print u
        print ''
