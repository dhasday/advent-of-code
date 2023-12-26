from typing import Dict

from aoc.common import helpers
from aoc.common.day_solver import DaySolver


class FallingBrick:
    def __init__(self, id, start_pos, end_pos):
        self.id = id
        self.initial_start_pos = start_pos
        self.initial_end_pos = end_pos
        self.min_z = start_pos[2]
        self.max_z = end_pos[2]
        self.supported_by = []

        assert self._all_directions_positive()

        self.all_positions = self._get_all_positions(start_pos, end_pos)

    @property
    def stable(self):
        return self.supported_by or self.min_z <= 1

    def __repr__(self):
        return f'{self.id} {self.initial_start_pos}~{self.initial_end_pos} ({self.all_positions})'

    def _all_directions_positive(self):
        x_pos = self.initial_start_pos[0] <= self.initial_end_pos[0]
        y_pos = self.initial_start_pos[1] <= self.initial_end_pos[1]
        z_pos = self.initial_start_pos[2] <= self.initial_end_pos[2]
        return x_pos and y_pos and z_pos

    def _get_all_positions(self, start_pos, end_pos):
        positions = set()
        for x in range(start_pos[0], end_pos[0] + 1):
            for y in range(start_pos[1], end_pos[1] + 1):
                for z in range(start_pos[2], end_pos[2] + 1):
                    positions.add((x, y, z))
        return positions

    def can_descend(self, other_bricks):
        if self.stable:
            return False

        next_positions = self._get_next_positions()

        for other_brick in other_bricks:
            if other_brick.id == self.id:
                continue

            if self.min_z > other_brick.max_z + 1:
                continue

            if any(v for v in other_brick.all_positions if v in next_positions):
                self.supported_by.append(other_brick.id)

        return not self.supported_by

    def do_descend(self, steps=1):
        self.all_positions = self._get_next_positions(steps)
        self.min_z = min(v[2] for v in self.all_positions)
        self.max_z = max(v[2] for v in self.all_positions)

    def _get_next_positions(self, steps=1):
        return set((v[0], v[1], v[2] - steps) for v in self.all_positions)


class BrickNode:
    def __init__(self, id: int):
        self.id = id
        self.supported_by = set()
        self.supports = set()

    def __hash__(self):
        return hash(self.id)


class Day22Solver(DaySolver):
    year = 2023
    day = 22

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        falling_bricks = []
        for idx, line in enumerate(lines):
            all_numbers = [int(v) for v in helpers.ALL_DIGITS_REGEX.findall(line)]
            falling_brick = FallingBrick(
                id=idx,
                start_pos=tuple(all_numbers[:3]),
                end_pos=tuple(all_numbers[3:]),
            )
            falling_bricks.append(falling_brick)

        self.simulate_falling_bricks(falling_bricks)

        # Convert the brick pile into a tree so it's easier (for me) to conceptualize
        tree = self._build_tree(falling_bricks)

        ans_one = self.count_can_disintegrate(tree)
        ans_two = self.num_fall_when_disintegrate_any(tree)

        return ans_one, ans_two

    def simulate_falling_bricks(self, falling_bricks):
        unstable_bricks = [fb for fb in falling_bricks if not fb.stable]
        unstable_bricks = sorted(unstable_bricks, key=lambda b: b.min_z)
        stable_bricks = [fb for fb in falling_bricks if fb.stable]
        max_stable_z = max(fb.max_z for fb in stable_bricks) if stable_bricks else 0
        while unstable_bricks:
            min_z = unstable_bricks[0].min_z

            now_stable = []
            for brick in unstable_bricks:
                if brick.min_z == min_z:
                    # Instantly drop close to the relevant range
                    if brick.min_z > max_stable_z + 1:
                        brick.do_descend(brick.min_z - max_stable_z - 1)

                    # Once at the right level check if we can descend more
                    if brick.can_descend(stable_bricks):
                        brick.do_descend()

                    # Lock the brick in place if it is stable now
                    if brick.stable:
                        stable_bricks.append(brick)
                        now_stable.append(brick)

            # Remove bricks that are now stable and update max z
            for brick in now_stable:
                unstable_bricks.remove(brick)
                max_stable_z = max(max_stable_z, brick.max_z)

    def count_can_disintegrate(self, tree):
        total = 0

        for node in tree.values():
            can_remove = True
            for node_2 in node.supports:
                if {node} == node_2.supported_by:
                    can_remove = False
            if can_remove:
                total += 1

        return total

    def num_fall_when_disintegrate_any(self, tree):
        total = 0
        for node in tree.values():
            removed = {node}
            to_visit = list(node.supports)
            while to_visit:
                cur = to_visit.pop()
                if cur.supported_by.difference(removed):
                    continue

                total += 1
                removed.add(cur)
                to_visit.extend(cur.supports)
        return total

    def _build_tree(self, bricks) -> Dict[int, BrickNode]:
        tree = {}  # id: BrickNode

        for brick in bricks:
            if brick.id not in tree:
                cur = BrickNode(brick.id)
                tree[brick.id] = cur
            else:
                cur = tree[brick.id]
            for supported_by in brick.supported_by:
                if supported_by not in tree:
                    prev = BrickNode(supported_by)
                    tree[supported_by] = prev

                other = tree[supported_by]
                cur.supported_by.add(other)
                other.supports.add(cur)

        return tree
