from aoc.common.day_solver import DaySolver
from aoc.dec2020.common.game_console import GameConsole


class Day08Solver(DaySolver):
    year = 2020
    day = 8

    def solve_puzzles(self):
        instructions = self.load_all_input_lines()
        console = GameConsole(instructions)

        ans_one = console.run_until_stop()

        target_pos = len(instructions)
        ans_two = 'ERROR'
        for i in range(target_pos):
            ins = console.get_instruction(i)
            if not ins.alter_instruction():
                continue

            console.reset()
            acc = console.run_until_stop()

            if console.cur_ins == target_pos:
                ans_two = acc
                break

            ins.alter_instruction()

        return ans_one, ans_two
