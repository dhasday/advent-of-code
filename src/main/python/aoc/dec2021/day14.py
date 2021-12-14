from collections import Counter, defaultdict

from aoc.common.day_solver import DaySolver


class Day14Solver(DaySolver):
    year = 2021
    day = 14

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        template = lines[0]
        pair_counts = defaultdict(lambda: 0)
        for i in range(len(template) - 1):
            pair_counts[template[i:i+2]] += 1

        mappings = {}
        for line in lines[2:]:
            a, b = line.split(' -> ')
            mappings[a] = b

        for _ in range(10):
            pair_counts = self._apply_mappings(pair_counts, mappings)
        part_1 = self._calculate_answer(pair_counts, template[-1])

        for _ in range(30):
            pair_counts = self._apply_mappings(pair_counts, mappings)
        part_2 = self._calculate_answer(pair_counts, template[-1])

        return part_1, part_2

    def _apply_mappings(self, pair_counts, mappings):
        new_pair_counts = defaultdict(lambda: 0)

        for pair, cnt in pair_counts.items():
            val = mappings[pair]
            new_pair_counts[pair[0] + val] += cnt
            new_pair_counts[val + pair[1]] += cnt

        return new_pair_counts

    def _calculate_answer(self, pair_counts, last_letter):
        letter_counts = Counter()

        for p, c in pair_counts.items():
            letter_counts[p[0]] += c

        letter_counts[last_letter] += 1

        return max(letter_counts.values()) - min(letter_counts.values())
