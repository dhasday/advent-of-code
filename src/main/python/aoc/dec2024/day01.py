from collections import defaultdict

from aoc.common.day_solver import DaySolver


class Day01Solver(DaySolver):
    year = 2024
    day = 1

    def solve_puzzles(self):
        lines = self.load_all_input_lines()
        list_one = []
        list_two = []
        counts = defaultdict(int)

        for line in lines:
            split_line = line.split(' ')

            a = int(split_line[0])
            b = int(split_line[-1])

            list_one.append(a)
            list_two.append(b)
            counts[b] += 1

        list_one = sorted(list_one)
        list_two = sorted(list_two)

        ans_one = 0
        ans_two = 0

        for i in range(len(list_one)):
            ans_one += abs(list_one[i] - list_two[i])
            ans_two += list_one[i] * counts[list_one[i]]

        return ans_one, ans_two
