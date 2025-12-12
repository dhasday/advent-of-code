import argparse
import os
from os.path import exists

MIN_YEAR = 2015
MAX_YEAR = 2100

MIN_DAY = 1
MAX_DAY = 25

PUZZLE_DAYS_IN_YEAR = {
    2015: 25,
    2016: 25,
    2017: 25,
    2018: 25,
    2019: 25,
    2020: 25,
    2021: 25,
    2022: 25,
    2023: 25,
    2024: 25,
    2025: 12,
}

parser = argparse.ArgumentParser(
    description='Generates the skeleton for the specified day',
)
parser.add_argument('year', type=int, metavar=f'[{MIN_YEAR}-{MAX_YEAR}]')
parser.add_argument('day', type=int, metavar=f'[{MIN_DAY}-{MAX_DAY} (varies by year)]')
parser.add_argument('--force', required=False, action='store_true', default=False)
parser.add_argument('--skip', required=False, action='store_true', default=False)


def run():
    parsed = parser.parse_args()

    year = parsed.year
    day = parsed.day
    force = parsed.force
    skip = parsed.skip

    if MIN_YEAR > year or MAX_YEAR < year:
        print(f'Invalid argument: year must be between {MIN_YEAR} and {MAX_YEAR}. You entered {year}')
        exit(1)

    max_day_for_year = PUZZLE_DAYS_IN_YEAR[year]
    if MIN_DAY > day or max_day_for_year < day:
        print(f'Invalid argument: day must be between {MIN_DAY} and {max_day_for_year}. You entered {day}')
        exit(1)

    _init_year_if_missing(year)

    solver_file = _build_filename(f'src/main/python/aoc/dec{year}/day{day:02d}.py')
    solver_contents = _get_solver_file_contents(year, day)
    _create_file(solver_file, solver_contents, 'solver class', force, skip)

    input_file = _build_filename(f'src/main/resources/dec{year}/{day}-input')
    _create_file(input_file, '', 'input file', force, skip)

    example_file = input_file + '-example'
    _create_file(example_file, '', 'example input file', force, skip)
    _uncomment_class_in_init(year, day)


def _init_year_if_missing(year):
    src_dir = _build_filename(f'src/main/python/aoc/dec{year}')
    if not os.path.exists(src_dir):
        os.mkdir(src_dir)

    init_file = f'{src_dir}/__init__.py'
    if not exists(init_file):
        init_contents = _get_init_file_contents(year)
        with open(init_file, 'w') as f:
            f.write(init_contents)

    input_dir = _build_filename(f'src/main/resources/dec{year}')
    if not os.path.exists(input_dir):
        os.mkdir(input_dir)


def _build_filename(path):
    return f'{os.path.dirname(__file__)}/{path}'


def _get_init_file_contents(year):
    contents = []

    max_day = PUZZLE_DAYS_IN_YEAR[year]

    for i in range(1, max_day + 1):
        contents.append(f'# from .day{i:02d} import Day{i:02d}Solver')
        if i % 5 == 0:
            contents.append('')

    if max_day % 5 != 0:
        contents.append('')

    return '\n'.join(contents)

def _get_solver_file_contents(year, day):
    return f"""from aoc.common.day_solver import DaySolver


class Day{day:02d}Solver(DaySolver):
    year = {year}
    day = {day}

    def setup(self):
        pass

    def solve_puzzle_one(self):
        # line = self.load_only_input_line(example=True)
        line = self.load_only_input_line()
        # lines = self.load_all_input_lines(example=True)
        lines = self.load_all_input_lines()

        return 'TODO'

    def solve_puzzle_two(self):
        # line = self.load_only_input_line(example=True)
        line = self.load_only_input_line()
        # lines = self.load_all_input_lines(example=True)
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
