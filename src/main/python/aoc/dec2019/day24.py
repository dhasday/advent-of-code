from aoc.common.day_solver import DaySolver

EMPTY_LAYER = '.' * 25


class Day24Solver(DaySolver):
    year = 2019
    day = 24

    def solve_puzzle_one(self):
        lines = self.load_all_input_lines()

        state = ''.join(lines)

        seen = set()
        while state not in seen:
            seen.add(state)
            next_state = ''
            for offset in range(25):
                cur_val = state[offset]
                row = offset // 5
                col = offset % 5

                adj_bugs = 0

                if col > 0:
                    adj_bugs += 1 if state[offset - 1] == '#' else 0
                if col < 4:
                    adj_bugs += 1 if state[offset + 1] == '#' else 0
                if row > 0:
                    adj_bugs += 1 if state[offset - 5] == '#' else 0
                if row < 4:
                    adj_bugs += 1 if state[offset + 5] == '#' else 0

                if cur_val == '#':
                    next_state += '#' if adj_bugs == 1 else '.'
                else:
                    next_state += '#' if adj_bugs in [1, 2] else '.'

            state = next_state

        rating = 0
        points = 1
        for val in state:
            if val == '#':
                rating += points
            points *= 2

        return rating

    def solve_puzzle_two(self):
        state = [''.join(self.load_all_input_lines())]

        for _ in range(200):
            # Pad with extra layer on each end for expansion
            test_state = [EMPTY_LAYER] + state + [EMPTY_LAYER]
            num_layers = len(test_state)

            next_state = []
            for i in range(num_layers):
                next_layer = ''
                for idx in range(25):
                    next_layer += self._get_next_value_recursive(
                        idx // 5,
                        idx % 5,
                        test_state[i - 1] if i > 0 else None,
                        test_state[i],
                        test_state[i + 1] if i < num_layers - 1 else None,
                    )
                next_state.append(next_layer)

            # Prune empty layers
            while next_state[0] == EMPTY_LAYER:
                next_state = next_state[1:]
            while next_state[-1] == EMPTY_LAYER:
                next_state = next_state[:-1]

            state = next_state

        return len(''.join(state).replace('.', ''))

    def _get_next_value_recursive(self, row, col, layer_up, cur_layer, layer_down):
        if col == 2 and row == 2:
            return '.'

        adj_bugs = 0
        offset = row * 5 + col
        cur_val = cur_layer[offset]

        if col > 0:
            adj_bugs += 1 if cur_layer[offset - 1] == '#' else 0
        if col < 4:
            adj_bugs += 1 if cur_layer[offset + 1] == '#' else 0
        if row > 0:
            adj_bugs += 1 if cur_layer[offset - 5] == '#' else 0
        if row < 4:
            adj_bugs += 1 if cur_layer[offset + 5] == '#' else 0

        if layer_up is not None:
            if col == 0:
                adj_bugs += 1 if layer_up[11] == '#' else 0  # 2, 1
            elif col == 4:
                adj_bugs += 1 if layer_up[13] == '#' else 0  # 2, 3

            if row == 0:
                adj_bugs += 1 if layer_up[7] == '#' else 0  # 1, 2
            elif row == 4:
                adj_bugs += 1 if layer_up[17] == '#' else 0  # 3, 2

        if layer_down is not None:
            if row == 1 and col == 2:
                for i in range(5):
                    adj_bugs += 1 if layer_down[i] == '#' else 0
            elif row == 2 and col == 1:
                for i in range(5):
                    adj_bugs += 1 if layer_down[i * 5] == '#' else 0
            elif row == 2 and col == 3:
                for i in range(5):
                    adj_bugs += 1 if layer_down[i * 5 + 4] == '#' else 0
            elif row == 3 and col == 2:
                for i in range(5):
                    adj_bugs += 1 if layer_down[20 + i] == '#' else 0

        if cur_val == '#':
            return '#' if adj_bugs == 1 else '.'
        else:
            return '#' if adj_bugs in [1, 2] else '.'


if __name__ == '__main__':
    Day24Solver().print_results()
