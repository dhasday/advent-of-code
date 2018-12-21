from aoc.common.day_solver import DaySolver

INPUT = '633601'

INITIAL_RECIPES = [3, 7]


class Day14Solver(DaySolver):
    year = 2018
    day = 14

    def solve_puzzles(self):
        scores = list(INITIAL_RECIPES)

        elf_one, elf_two = 0, 1

        target = [int(c) for c in INPUT]
        target_start = None
        min_length = int(INPUT) + 10
        while len(scores) < min_length or not target_start:
            r1 = scores[elf_one]
            r2 = scores[elf_two]

            new_recipe = r1 + r2
            scores.extend(divmod(new_recipe, 10) if new_recipe >= 10 else (new_recipe,))

            elf_one = (elf_one + r1 + 1) % len(scores)
            elf_two = (elf_two + r2 + 1) % len(scores)

            if not target_start:
                if scores[-len(target):] == target:
                    target_start = len(scores) - len(target)
                elif scores[-len(target) - 1: -1] == target:
                    target_start = len(scores) - len(target) - 1

        ans_one = ''.join(str(s) for s in scores[int(INPUT): int(INPUT) + 10])

        return ans_one, target_start
