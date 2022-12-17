from aoc.common.day_solver import DaySolver

ROCK_PATTERNS = [
    {
        (2, 4), (3, 4), (4, 4), (5, 4)
    },
    {
        (3, 6),
        (2, 5), (3, 5), (4, 5),
        (3, 4),
    },
    {
        (4, 6),
        (4, 5),
        (2, 4), (3, 4), (4, 4),
    },
    {
        (2, 7),
        (2, 6),
        (2, 5),
        (2, 4),
    },
    {
        (2, 5), (3, 5),
        (2, 4), (3, 4),
    },
]


class RockState(object):
    rock_idx = 0
    line_idx = 0
    highest_rock = 0

    def __init__(self, line):
        self.line = line
        self.frozen_rocks = {(i, 0) for i in range(7)}

        self.rock_to_height = {
            0: 0,
        }

    def drop_rock(self):
        cur_rock = self._get_rock()

        should_freeze = False
        while not should_freeze:
            cur_rock = self._apply_wind(cur_rock)
            cur_rock, should_freeze = self._apply_drop(cur_rock)

        for stone in cur_rock:
            self.highest_rock = max(self.highest_rock, stone[1])
            self.frozen_rocks.add(stone)

    def _get_rock(self):
        cur_rock = set()
        for loc in ROCK_PATTERNS[self.rock_idx]:
            cur_rock.add((loc[0], loc[1] + self.highest_rock))
        self.rock_idx = (self.rock_idx + 1) % len(ROCK_PATTERNS)
        return cur_rock

    def _apply_wind(self, cur_rock):
        offset = -1 if self.line[self.line_idx] == '<' else 1

        next_rock = set()
        for cur_stone in cur_rock:
            next_stone = cur_stone[0] + offset, cur_stone[1]
            if 0 > next_stone[0] or 6 < next_stone[0] or next_stone in self.frozen_rocks:
                next_rock = cur_rock
                break
            next_rock.add(next_stone)

        self.line_idx = (self.line_idx + 1) % len(self.line)
        return next_rock

    def _apply_drop(self, cur_rock):
        next_rock = set()
        for cur_stone in cur_rock:
            next_stone = cur_stone[0], cur_stone[1] - 1
            if next_stone in self.frozen_rocks:
                return cur_rock, True
            next_rock.add(next_stone)
        return next_rock, False

    def find_cycle(self):
        cur_rock = None
        rock_count = 0

        rocks = []
        heights = []
        for _ in range(2):
            started = False
            while not started or self.line_idx != 0:
                started = True
                if cur_rock is None:
                    cur_rock = self._get_rock()
                    rock_count += 1

                cur_rock = self._apply_wind(cur_rock)
                cur_rock, should_freeze = self._apply_drop(cur_rock)

                if should_freeze:
                    for stone in cur_rock:
                        self.highest_rock = max(self.highest_rock, stone[1])
                        self.frozen_rocks.add(stone)
                    cur_rock = None
                    self.rock_to_height[rock_count] = self.highest_rock
            rocks.append(rock_count)
            heights.append(self.highest_rock)

        cycle_rocks = rocks[1] - rocks[0]
        init_rocks = rocks[0] - cycle_rocks
        cycle_height = self.highest_rock - heights[0]

        return init_rocks, cycle_rocks, cycle_height


class Day17Solver(DaySolver):
    year = 2022
    day = 17

    def solve_puzzle_one(self):
        line = self.load_only_input_line()

        state = RockState(line)
        for i in range(2022):
            state.drop_rock()
        return state.highest_rock

    def solve_puzzle_two(self):
        line = self.load_only_input_line()

        state = RockState(line)

        init_rocks, cycle_rocks, cycle_height_delta = state.find_cycle()

        # Find the number of rocks we'll need to process before we can just add height delta * cycles
        target_rocks = 1000000000000
        num_cycles_skip = ((target_rocks - init_rocks) // cycle_rocks) - 1
        num_rocks = target_rocks - (num_cycles_skip * cycle_rocks)

        # There's likely an easier way to do this, but my math wasn't working out properly and we've
        # already checked the height of num_rocks when determining the cycle data
        return state.rock_to_height[num_rocks] + (cycle_height_delta * num_cycles_skip)
