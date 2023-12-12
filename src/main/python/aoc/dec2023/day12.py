from aoc.common.day_solver import DaySolver


GOOD = '.'
BROKEN = '#'
UNKNOWN = '?'


class Day12Solver(DaySolver):
    year = 2023
    day = 12

    memo = {}

    def solve_puzzle_one(self):
        lines = self.load_all_input_lines()

        total = 0
        for line in lines:
            seq, parts = line.split(' ')
            parts = [int(p) for p in parts.split(',')]

            num_possible = self._num_possible_arrangements(seq, parts)
            total += num_possible

        return total

    def solve_puzzle_two(self):
        lines = self.load_all_input_lines()

        total = 0
        for line in lines:
            seq, parts = line.split(' ')
            parts = [int(p) for p in parts.split(',')]

            expanded_seq = ((seq + UNKNOWN) * 5)[:-1]
            expanded_parts = parts * 5

            num_possible = self._num_possible_arrangements(expanded_seq, expanded_parts)
            total += num_possible

        return total

    def _num_possible_arrangements(self, seq, parts):
        memo_key = tuple([seq, *parts])
        if memo_key in self.memo:
            return self.memo[memo_key]

        # We're run out of parts to find
        if len(parts) == 0:
            if '#' in seq:
                # There's still a broken spring, then we didn't match
                self.memo[memo_key] = 0
                return 0
            else:
                # There are no broken springs remaining, then we did match
                self.memo[memo_key] = 1
                return 1

        # If we don't meet the minimum length to fully match, short circuit failure
        if len(seq) < sum(parts) + len(parts) - 1:
            self.memo[memo_key] = 0
            return 0

        # There are broken sections remaining, so if there aren't any possible broken strings, we don't match
        first_broken = seq.find(BROKEN)
        if seq.find(UNKNOWN) == -1 and first_broken == -1:
            self.memo[memo_key] = 0
            return 0

        # If the first spring is good, skip to the next value
        if seq[0] == '.':
            return self._num_possible_arrangements(seq[1:], parts)

        count = 0
        for i in range(len(seq) if first_broken == -1 else first_broken + 1):
            remaining_seq = seq[i:]
            cur_block = remaining_seq[0:parts[0]]
            if '.' not in cur_block and len(cur_block) == parts[0]:
                if len(remaining_seq) == parts[0]:
                    if len(parts) == 1:
                        count += 1
                elif remaining_seq[parts[0]] != BROKEN:
                    count += self._num_possible_arrangements(remaining_seq[parts[0] + 1:], parts[1:])

        self.memo[memo_key] = count
        return count
