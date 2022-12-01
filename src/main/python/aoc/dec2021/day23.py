from collections import deque
from copy import deepcopy

from aoc.common.day_solver import DaySolver

MOVEMENT_COST_MAP = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
TARGET_X = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
X_TO_HOLE = {2: 'A', 4: 'B', 6: 'C', 8: 'D'}
TOP_TITLE = 'T'
PLACEHOLDER_CHAR = '.'


class Day23Solver(DaySolver):
    year = 2021
    day = 23

    # #############
    # #...........#
    # ###B#A#B#C###
    #   #D#A#D#C#
    #   #########
    def solve_puzzle_one(self):
        # Manually calculated
        # A C2-1 -> T-0
        # A C2-2 -> T-1
        # B C1-1 -> C2-2
        # B C3-1 -> C2-1
        # C C4-1 -> T-9
        # C C4-2 -> T-5
        # D C3-2 -> C4-2
        # C T-5  -> C3-2
        # C T-9  -> C3-1
        # D C1-2 -> C4-1
        # A T-1  -> C1-2
        # A T-0  -> C1-1
        return 16506
        # Example - 12521
        initial_state = '...........BACDBCDA'
        target_state = '...........AABBCCDD'
        return self._solve_state(initial_state, target_state, 14000)

        # Real - 16506
        initial_state = '...........BDAABDCC'
        target_state = '...........AABBCCDD'
        return self._solve_state(initial_state, target_state, 20000)

    def solve_puzzle_two(self):
        return 48304
        # #############
        # #...........#
        # ###B#A#B#C###
        #   #D#C#B#A#
        #   #D#B#A#C#
        #   #D#A#D#C#
        #   #########

        # noinspection SpellCheckingInspection
        initial_state = '...........BDDDACBABBADCACC'
        target_state = '...........AAAABBBBCCCCDDDD'

        return self._solve_state(initial_state, target_state, 50000)

    def _solve_state(self, initial, target, max_cost):
        to_check = deque()
        to_check.append(initial)
        state_costs = {initial: 0}

        while to_check:
            cur_state = to_check.popleft()
            cur_cost = state_costs[cur_state]
            print(len(to_check), cur_cost, cur_state)

            cur_top, cur_holes = self._from_state_string(cur_state)
            available_moves = self._get_available_moves(cur_top, cur_holes)
            for move in available_moves:
                adj_state = self._apply_move(cur_top, cur_holes, move)
                adj_cost = state_costs.get(adj_state)
                new_cost = cur_cost + move[4]
                if (adj_cost is None or new_cost < adj_cost) and new_cost < max_cost:
                    state_costs[adj_state] = new_cost
                    if adj_state not in to_check:
                        to_check.append(adj_state)

                if adj_state == target:
                    print(adj_state, adj_cost)

        return state_costs.get(target, 'ERROR')

    def _get_available_moves(self, top, holes):
        available_moves = self._get_available_moves_from_hallway(top, holes)

        for hole, values in holes.items():
            available_moves.extend(self._get_available_moves_for_hole(top, hole, values))

        return available_moves

    def _get_available_moves_from_hallway(self, top, holes):
        available_moves = []
        # Check move from hallway to correct hole
        for idx, val in enumerate(top):
            if val == PLACEHOLDER_CHAR:
                continue

            if holes[val][0] != '.':
                continue

            if self._can_move_to_target_hole(top, holes[val], idx, val):
                pass
            if self._can_move_to_target_hole(top, holes[val], idx, val):
                target_hole = TARGET_X.get(val)
                cost = abs(idx - target_hole) + 1
                available_moves.append(
                    ('T', idx, val, 0, cost * MOVEMENT_COST_MAP[val])
                )
        return available_moves

    def _get_available_moves_for_hole(self, top, hole, values):
        available_moves = []

        hole_idx = TARGET_X[hole]
        for idx, val in enumerate(values):
            if val == PLACEHOLDER_CHAR:
                continue

            if idx == 0:
                possible_exit_moves = self._get_possible_exit_moves(hole_idx, top, val)
                move_cost = MOVEMENT_COST_MAP[val]
                for move in possible_exit_moves:
                    available_moves.append((hole, idx, move[0], move[1], move_cost * move[2]))
            if idx > 0 and values[idx - 1] == PLACEHOLDER_CHAR:
                available_moves.append((hole, idx, hole, idx - 1, MOVEMENT_COST_MAP[val]))
            if idx < len(values) - 1 and values[idx + 1] == PLACEHOLDER_CHAR:
                available_moves.append((hole, idx, hole, idx + 1, MOVEMENT_COST_MAP[val]))
        return available_moves

    def _can_move_to_target_hole(self, top, hole, idx, val):
        # if hole is empty or only has val
        for v in hole:
            if v not in (PLACEHOLDER_CHAR, val):
                return False

        target_hole = TARGET_X.get(val)
        if idx < target_hole:
            for v in top[idx:target_hole]:
                if v != '.':
                    return False
        else:
            for v in top[idx:target_hole:-1]:
                if v != '.':
                    return False

        return True

    def _get_possible_exit_moves(self, hole_idx, top, val):
        possible_exits = []
        if top[hole_idx] != PLACEHOLDER_CHAR:
            return possible_exits

        for i, top_val in enumerate(top[hole_idx + 1:], 1):
            if top_val != '.':
                break
            target_idx = hole_idx + i
            if target_idx not in X_TO_HOLE:
                possible_exits.append(
                    ('T', target_idx, i + 1)
                )

        for i, top_val in enumerate(top[:hole_idx][::-1], 1):
            if top_val != '.':
                break
            target_idx = hole_idx - i
            if target_idx not in X_TO_HOLE:
                possible_exits.append(
                    ('T', target_idx, i + 1)
                )

        return possible_exits

    def _stringify_state(self, top, holes):
        state = ''.join(top)
        state += ''.join(holes['A'])
        state += ''.join(holes['B'])
        state += ''.join(holes['C'])
        state += ''.join(holes['D'])
        return state

    def _from_state_string(self, state):
        top = [c for c in state[:11]]
        length = (len(state) - 11) // 4
        bound_2 = 11 + length
        bound_3 = bound_2 + length
        bound_4 = bound_3 + length
        holes = {
            'A': [c for c in state[11:bound_2]],
            'B': [c for c in state[bound_2:bound_3]],
            'C': [c for c in state[bound_3:bound_4]],
            'D': [c for c in state[bound_4:]],
        }
        return top, holes

    def _apply_move(self, cur_top, cur_holes, move):
        next_top = cur_top.copy()
        next_holes = deepcopy(cur_holes)

        col_1 = move[0]
        idx_1 = move[1]
        col_2 = move[2]
        idx_2 = move[3]

        if col_1 == 'T':
            next_top[idx_1] = cur_top[idx_2] if col_2 == 'T' else cur_holes[col_2][idx_2]
        else:
            next_holes[col_1][idx_1] = cur_top[idx_2] if col_2 == 'T' else cur_holes[col_2][idx_2]

        if col_2 == 'T':
            next_top[idx_2] = cur_top[idx_1] if col_1 == 'T' else cur_holes[col_1][idx_1]
        else:
            next_holes[col_2][idx_2] = cur_top[idx_1] if col_1 == 'T' else cur_holes[col_1][idx_1]

        return self._stringify_state(next_top, next_holes)
