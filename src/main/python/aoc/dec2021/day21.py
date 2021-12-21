from aoc.common.day_solver import DaySolver

PLAYER_1_START = 1
PLAYER_2_START = 3

DIE_RESULTS = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1,
}


class Day21Solver(DaySolver):
    year = 2021
    day = 21

    deterministic_die = 0
    memo = {}

    def solve_puzzle_one(self):
        self.deterministic_die = 0
        num_rolls = 0

        pos_1 = PLAYER_1_START
        pos_2 = PLAYER_2_START
        score_1 = 0
        score_2 = 0
        p1_turn = True

        while score_1 < 1000 and score_2 < 1000:
            total = self._roll_deterministic_dice(3)
            num_rolls += 3

            if p1_turn:
                pos_1, score_1 = self._apply_result(pos_1, score_1, total)
            else:
                pos_2, score_2 = self._apply_result(pos_2, score_2, total)

            p1_turn = not p1_turn

        loser_score = score_1 if p1_turn else score_2
        return num_rolls * loser_score

    def solve_puzzle_two(self):
        p1_wins, p2_wins = self._count_wins(PLAYER_1_START, 0, PLAYER_2_START, 0)
        return max(p1_wins, p2_wins)

    def _roll_deterministic_dice(self, num_rolls):
        total = 0
        for _ in range(num_rolls):
            self.deterministic_die += 1
            self.deterministic_die %= 100
            total += self.deterministic_die if self.deterministic_die else 100
        return total

    def _apply_result(self, pos, score, num):
        pos += num
        pos %= 10
        score += pos if pos else 10
        return pos, score

    def _count_wins(self, pos_1, score_1, pos_2, score_2, p1_turn=True):
        if score_1 >= 21:
            return 1, 0
        if score_2 >= 21:
            return 0, 1

        node = pos_1, score_1, pos_2, score_2, p1_turn
        if node in self.memo:
            return self.memo[node]

        p1_wins = 0
        p2_wins = 0
        for num, cnt in DIE_RESULTS.items():
            if p1_turn:
                p1, s1 = self._apply_result(pos_1, score_1, num)
                w1, w2 = self._count_wins(p1, s1, pos_2, score_2, False)
            else:
                p2, s2 = self._apply_result(pos_2, score_2, num)
                w1, w2 = self._count_wins(pos_1, score_1, p2, s2, True)

            p1_wins += w1 * cnt
            p2_wins += w2 * cnt
        self.memo[node] = p1_wins, p2_wins

        return p1_wins, p2_wins
