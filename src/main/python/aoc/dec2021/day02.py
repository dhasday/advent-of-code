from aoc.common.day_solver import DaySolver


class Day02Solver(DaySolver):
    year = 2021
    day = 2

    def solve_puzzles(self):
        cur_pos = 0
        cur_depth = 0
        cur_aim = 0

        for line in self.load_all_input_lines():
            cmd, num = line.split(' ')
            num = int(num)

            if cmd == 'forward':
                cur_pos += num
                cur_depth += (cur_aim * num)
            elif cmd == 'up':
                cur_aim -= num
            elif cmd == 'down':
                cur_aim += num

        part_1 = cur_pos * cur_aim
        part_2 = cur_pos * cur_depth
        return part_1, part_2
