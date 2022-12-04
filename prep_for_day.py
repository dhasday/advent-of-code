import argparse
import os
from os.path import exists

parser = argparse.ArgumentParser(
    description='Generates the skeleton for the specified day',
)
parser.add_argument('year', type=int)
parser.add_argument('day', type=int)
parser.add_argument('--force', required=False, action='store_true', default=False)


def run():
    parsed = parser.parse_args()

    year = parsed.year
    day = parsed.day
    force = parsed.force

    _create_solver_file(year, day, force)
    _create_input_file(year, day, force)
    _uncomment_class_in_init(year, day)


def _build_filename(path):
    return f'{os.path.dirname(__file__)}/{path}'


def _create_solver_file(year, day, force):
    contents = f"""from aoc.common.day_solver import DaySolver


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

    filename = _build_filename(f'src/main/python/aoc/dec{year}/day{day:02d}.py')
    if exists(filename):
        if force:
            print('Overwriting existing solver class because --force was specified')
        else:
            print('FAIL: Solver class already exists, re-run with --force to overwrite')
            exit(1)

    with open(filename, 'w') as f:
        f.write(contents)


def _create_input_file(year, day, force):
    filename = _build_filename(f'src/main/resources/dec{year}/{day}-input')

    if exists(filename):
        if force:
            print('Overwriting existing input file because --force was specified')
        else:
            print('FAIL: Input file already exists, re-run with --force to overwrite')
            exit(1)

    with open(filename, 'w'):
        pass


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
