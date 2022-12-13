import functools

from aoc.common.day_solver import DaySolver


class Day13Solver(DaySolver):
    year = 2022
    day = 13

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        divider_one = [[2]]
        divider_two = [[6]]

        p1_total = 0
        sorted_packets = [divider_one, divider_two]
        cur_pair_index = 0
        for i in range(0, len(lines), 3):
            cur_pair_index += 1
            line_1 = eval(lines[i])
            line_2 = eval(lines[i+1])

            if self._compare_packets(line_1, line_2) <= 0:
                p1_total += cur_pair_index

            sorted_packets.append(line_1)
            sorted_packets.append(line_2)

        sorted_packets = sorted(sorted_packets, key=functools.cmp_to_key(self._compare_packets))

        distress_signal = (sorted_packets.index(divider_one) + 1) * (sorted_packets.index(divider_two) + 1)

        return p1_total, distress_signal

    def _compare_packets(self, a, b):
        # If we've got ints, just compare them
        if isinstance(a, int) and isinstance(b, int):
            return a - b

        # Make sure we've got 2 lists to compare
        if isinstance(a, int):
            a = [a]
        if isinstance(b, int):
            b = [b]

        # Compare each list item and then the lengths, breaking at the first difference
        for i in range(min(len(a), len(b))):
            item_result = self._compare_packets(a[i], b[i])
            if item_result != 0:
                return item_result
        return len(a) - len(b)


Day13Solver().print_results()