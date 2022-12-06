import argparse
import os
from os.path import exists

parser = argparse.ArgumentParser(
    description='Generates the skeleton for the specified day',
)
parser.add_argument('year', type=int)
parser.add_argument('day', type=int)
parser.add_argument('--force', required=False, action='store_true', default=False)
parser.add_argument('--skip', required=False, action='store_true', default=False)


def run():
    parsed = parser.parse_args()

    year = parsed.year
    day = parsed.day
    force = parsed.force
    skip = parsed.skip

    solver_file = _build_filename(f'src/main/python/aoc/dec{year}/day{day:02d}.py')
    solver_contents = _get_solver_file_contents(year, day)
    _create_file(solver_file, solver_contents, 'solver class', force, skip)

    input_file = _build_filename(f'src/main/resources/dec{year}/{day}-input')
    _create_file(input_file, '', 'input file', force, skip)

    example_file = input_file + '-example'
    _create_file(example_file, '', 'example input file', force, skip)
    _uncomment_class_in_init(year, day)


def _build_filename(path):
    return f'{os.path.dirname(__file__)}/{path}'


def _get_solver_file_contents(year, day):
    return f"""from aoc.common.day_solver import DaySolver


class Day{day:02d}Solver(DaySolver):
    year = {year}
    day = {day}

    def setup(self):
        pass

    def solve_puzzle_one(self):
        # line = self.load_only_input_line(example=True)
        # lines = self.load_all_input_lines(example=True)
        line = self.load_only_input_line()
        lines = self.load_all_input_lines()

        return 'TODO'

    def solve_puzzle_two(self):
        # line = self.load_only_input_line(example=True)
        # lines = self.load_all_input_lines(example=True)
        line = self.load_only_input_line()
        lines = self.load_all_input_lines()

        return 'TODO'


Day{day:02d}Solver().print_results()
"""


def _create_file(filename, contents, display_name, force, skip):
    if exists(filename):
        if skip:
            print(f'Skipping existing {display_name} because --skip was specified')
        elif force:
            print(f'Overwriting existing {display_name} because --force was specified')
        else:
            print(f'FAIL: {display_name} already exists, re-run with --force to overwrite')
            exit(1)

    with open(filename, 'w') as f:
        f.write(contents)


def _uncomment_class_in_init(year, day):
    filename = _build_filename(f'src/main/python/aoc/dec{year}/__init__.py')

    with open(filename) as f:
        all_lines = [line for line in f]

    current_class_name = f'Day{day:02d}Solver'
    with open(filename, 'w') as f:
        for line in all_lines:
            to_write = line
            if current_class_name in line and line.startswith('# '):
                to_write = line[2:]
            f.write(to_write)


if __name__ == '__main__':
    run()
