from aoc.common.day_solver import DaySolver


class Day10Solver(DaySolver):
    year = 2015
    day = 10

    def solve_puzzles(self):
        current = self.load_only_input_line()

        for _ in range(40):
            current = self._look_say(current)

        ans_one = len(current)

        for _ in range(10):
            current = self._look_say(current)

        ans_two = len(current)

        return ans_one, ans_two

    def _look_say(self, input):
        output = ''

        cur_char = None
        cur_count = 0
        for c in input:
            if c == cur_char:
                cur_count += 1
            else:
                if cur_char:
                    output += str(cur_count) + str(cur_char)

                cur_char = c
                cur_count = 1

        output += str(cur_count) + str(cur_char)

        return output
