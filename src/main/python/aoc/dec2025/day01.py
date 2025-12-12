from aoc.common.day_solver import DaySolver


START_POSITION = 50

class Day01Solver(DaySolver):
    year = 2025
    day = 1

    def solve_puzzles(self):
        lines = self.load_all_input_lines()

        answer_one = 0
        answer_two = 0
        cur_pos = START_POSITION
        for line in lines:
            direction = line[0]
            num = int(line[1:])

            if direction == 'R':
                cur_pos += num
                if cur_pos >= 100:
                    answer_two += cur_pos // 100
                    cur_pos %= 100

            elif direction == 'L':
                if cur_pos == 0:
                    # Make sure we don't count this rotation since we've already counted this 0
                    answer_two -= 1

                cur_pos -= num
                if cur_pos < 0:
                    answer_two -= cur_pos // 100
                    cur_pos %= 100

                if cur_pos == 0:
                    answer_two += 1
            else:
                raise Exception(f'Unknown direction: {direction}')

            if cur_pos == 0:
                answer_one += 1

        return answer_one, answer_two
