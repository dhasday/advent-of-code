from aoc.common.day_solver import DaySolver


class Day06Solver(DaySolver):
    year = 2020
    day = 6

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        ans_one = 0
        ans_two = 0

        group = []
        for line in lines:
            if not line:
                ans_one += self._count_for_any_in_group(group)
                ans_two += self._count_for_all_in_group(group)
                group = []
            else:
                group.append(line)

        ans_one += self._count_for_any_in_group(group)
        ans_two += self._count_for_all_in_group(group)

        return ans_one, ans_two

    def _count_for_any_in_group(self, group):
        all_chars = set()
        for person in group:
            for c in person:
                all_chars.add(c)
        return len(all_chars)

    def _count_for_all_in_group(self, group):
        if not group:
            return 0
        if len(group) == 1:
            return len(group[0])
        matching_answers = {c for c in group[0]}

        for person in group[1:]:
            for ans in list(matching_answers):
                if ans not in person:
                    matching_answers.discard(ans)

        return len(matching_answers)
