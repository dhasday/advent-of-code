import itertools
from collections import deque

from aoc.common.day_solver import DaySolver


class Day22Solver(DaySolver):
    year = 2020
    day = 22

    def solve_puzzle_one(self):
        player_1, player_2 = self._load_input()
        winner = self._play_single_game(player_1, player_2)
        return self._calculate_score(player_1 if winner == 1 else player_2)

    def solve_puzzle_two(self):
        player_1, player_2 = self._load_input()

        # winner = 1
        winner = self._play_recursive_game(player_1, player_2)

        return self._calculate_score(player_1 if winner == 1 else player_2)

    def _load_input(self):
        player_1 = deque()
        player_2 = deque()

        end_player_1 = False
        for line in self.load_all_input_lines():
            if line == '':
                end_player_1 = True
            elif line.isnumeric():
                if not end_player_1:
                    player_1.append(int(line))
                else:
                    player_2.append(int(line))


            pass

        return player_1, player_2

    def _play_single_game(self, player_1, player_2):
        while player_1 and player_2:
            c1 = player_1.popleft()
            c2 = player_2.popleft()

            if c1 < c2:
                player_2.append(c2)
                player_2.append(c1)
            else:
                player_1.append(c1)
                player_1.append(c2)

        return 1 if player_1 else 2

    def _calculate_score(self, winning_player):

        total = 0
        cur_multiplier = 1
        while winning_player:
            total += winning_player.pop() * cur_multiplier
            cur_multiplier += 1

        return total

    def _play_recursive_game(self, player_1, player_2):
        seen_games = set()

        while player_1 and player_2:
            p1_str = ','.join(map(str, player_1))
            p2_str = ','.join(map(str, player_2))
            if (p1_str, p2_str) in seen_games:
                return 1
            seen_games.add((p1_str, p2_str))

            c1 = player_1.popleft()
            c2 = player_2.popleft()

            if len(player_1) >= c1 and len(player_2) >= c2:
                subgame_player_1 = deque(itertools.islice(player_1, 0, c1))
                subgame_player_2 = deque(itertools.islice(player_2, 0, c2))
                w = self._play_recursive_game(subgame_player_1, subgame_player_2)
            else:
                w = 1 if c1 > c2 else 2

            if w == 1:
                player_1.append(c1)
                player_1.append(c2)
            else:
                player_2.append(c2)
                player_2.append(c1)

        return 1 if player_1 else 2
