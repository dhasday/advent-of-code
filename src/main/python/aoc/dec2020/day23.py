from aoc.common.day_solver import DaySolver

INPUT = '247819356'


class Day23Solver(DaySolver):
    year = 2020
    day = 23

    def solve_puzzle_one(self):
        cups, head = self._load_cups(9)

        for _ in range(100):
            cups, head = self._simulate_move(cups, head, 9)

        ans_one = ''
        cur = cups[1]
        while cur != 1:
            ans_one += str(cur)
            cur = cups[cur]
        return ans_one

    def solve_puzzle_two(self):
        cups, head = self._load_cups(1000000)

        for _ in range(10000000):
            cups, head = self._simulate_move(cups, head, 1000000)

        one = cups[1]
        return one * cups[one]

    def _load_cups(self, max_cup):
        initial = list(map(int, INPUT))

        cups = [i + 1 for i in range(max_cup + 1)]
        for i, label in enumerate(initial[:-1]):
            cups[label] = initial[i + 1]
        head = initial[0]
        if max_cup > len(initial):
            cups[-1] = head
            cups[initial[-1]] = max(initial) + 1
        else:
            cups[initial[-1]] = head

        return cups, head

    def _simulate_move(self, cups, head, max_cup):
        cur = cups[head]
        cups[head] = cups[cups[cups[cur]]]
        picked_cups = cur, cups[cur], cups[cups[cur]]

        dest = max_cup if head == 1 else head - 1
        while dest in picked_cups:
            dest = max_cup if dest == 1 else dest - 1

        cups[cups[cups[cur]]] = cups[dest]
        cups[dest] = cur

        return cups, cups[head]
