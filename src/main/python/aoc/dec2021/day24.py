from aoc.common.day_solver import DaySolver


class Day24Solver(DaySolver):
    year = 2021
    day = 24

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        all_coeffs = []
        for idx in range((len(lines) // 18)):
            base_line_num = idx * 18
            coeff = (
                int(lines[base_line_num + 5].split(' ')[2]),
                int(lines[base_line_num + 15].split(' ')[2]),
            )
            all_coeffs.append(coeff)

        stack = []
        related = {}
        for idx, coeffs in enumerate(all_coeffs):
            if coeffs[0] > 0:
                stack.append((idx, coeffs[1]))
            else:
                i2, v2 = stack.pop()
                related[idx] = (i2, v2 + coeffs[0])

        max_value = [0] * len(all_coeffs)
        for idx, (idx_linked, delta) in related.items():
            max_value[idx] = min(9, 9 + delta)
            max_value[idx_linked] = min(9, 9 - delta)
        part_1 = ''.join([str(v) for v in max_value])

        min_value = [0] * len(all_coeffs)
        for idx, (idx_linked, delta) in related.items():
            min_value[idx] = max(1, 1 + delta)
            min_value[idx_linked] = max(1, 1 - delta)
        part_2 = ''.join([str(v) for v in min_value])
        return part_1, part_2
