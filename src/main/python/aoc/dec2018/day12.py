import re

from aoc.common.day_solver import DaySolver

INITIAL_STATE = '###....#..#..#......####.#..##..#..###......##.##..#...#.##.###.##.###.....#.###..#.#.##.#..#.#'
INPUT_REGEX = re.compile('([.#]{5}) => ([.#])')

PLANT = '#'
NO_PLANT = '.'


class Day12Solver(DaySolver):
    year = 2018
    day = 12

    def solve_puzzles(self):
        transitions = self._load_transitions()

        cur_state, first_index = self._process_n_iterations(transitions, INITIAL_STATE, 0, 20)
        ans_one = self._sum_plants(cur_state, first_index)

        # This could continue from where the first 20 left off, but not much gained by doing so
        cur_state, first_index = self._process_n_iterations(transitions, INITIAL_STATE, 0, 50000000000)
        ans_two = self._sum_plants(cur_state, first_index)

        return ans_one, ans_two

    def _load_transitions(self):
        transitions = {}

        for line in self.load_all_input_lines():
            parsed = INPUT_REGEX.match(line)

            transitions[parsed.group(1)] = parsed.group(2)

        return transitions

    def _process_n_iterations(self, transitions, initial_state, initial_offset, num_iterations):
        cur_state = initial_state
        cur_offset = initial_offset
        cur_iters = 0

        # Store seen states to find cycles
        seen_states = {
            cur_state: (cur_iters, cur_offset)
        }
        while cur_iters < num_iterations:
            cur_state, offset = self._perform_transitions(transitions, cur_state)
            cur_offset += offset
            cur_iters += 1

            if cur_state not in seen_states:
                seen_states[cur_state] = (cur_iters, cur_offset)
            else:
                # Get loop size and remaining iterations so we can shortcut calculations
                start_iter, start_offset = seen_states[cur_state]
                loop_size = cur_iters - start_iter
                remaining_iters = num_iterations - cur_iters

                # Find where we'll end up and how many loops it'll take
                loop_cycles = remaining_iters // loop_size
                loop_end_index = remaining_iters % loop_size

                loop_state = cur_state
                for i in range(loop_end_index + 1):
                    loop_state, offset = self._perform_transitions(transitions, loop_state)

                # If this wasn't a full cycle
                if loop_end_index != 0:
                    cur_offset += offset

                cur_offset = cur_offset + (loop_cycles * offset)
                break

        return cur_state, cur_offset

    def _perform_transitions(self, transitions, input):
        first_plant = input.find(PLANT)
        last_plant = input.rfind(PLANT)

        cur_state = (NO_PLANT * 4) + input[first_plant:last_plant + 1] + (NO_PLANT * 4)
        next_state = ''

        for i in range(2, len(cur_state) - 2):
            cur_input = cur_state[(i - 2):(i + 3)]
            next_state += transitions[cur_input]

        return next_state, first_plant - 2

    def _sum_plants(self, state, offset):
        sum_plants = 0

        for i in range(len(state)):
            if state[i] == PLANT:
                sum_plants += i + offset

        return sum_plants
