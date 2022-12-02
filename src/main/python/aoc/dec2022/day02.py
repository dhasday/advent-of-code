from aoc.common.day_solver import DaySolver


class Day02Solver(DaySolver):
    year = 2022
    day = 2

    P1_MAPPING = {
        'A X': 4,  # Rock + Draw
        'A Y': 8,  # Paper + Win
        'A Z': 3,  # Scissors + Lose
        'B X': 1,  # Rock + Lose
        'B Y': 5,  # Paper + Draw
        'B Z': 9,  # Scissors + Win
        'C X': 7,  # Rock + Win
        'C Y': 2,  # Paper + Lose
        'C Z': 6,  # Scissors + Draw
    }
    P2_MAPPING = {
        'A X': 3,  # Lose + Scissors
        'A Y': 4,  # Draw + Rock
        'A Z': 8,  # Win  + Paper
        'B X': 1,  # Lose + Rock
        'B Y': 5,  # Draw + Paper
        'B Z': 9,  # Win  + Scissors
        'C X': 2,  # Lose + Paper
        'C Y': 6,  # Draw + Scissors
        'C Z': 7,  # Win  + Rock
    }

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        p1_score = 0
        p2_score = 0
        for line in lines:
            p1_score += self.P1_MAPPING[line]
            p2_score += self.P2_MAPPING[line]

        return p1_score, p2_score
