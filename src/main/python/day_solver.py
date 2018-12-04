from abc import ABCMeta, abstractproperty
from time import time
import os

SLOW_ELAPSED_THRESHOLD = 1000


class DaySolver(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        super(DaySolver, self).__init__()

    def solve_puzzles(self):
        return self.solve_puzzle_one(), self.solve_puzzle_two()

    @abstractproperty
    def year(self):
        pass

    @abstractproperty
    def day(self):
        pass

    def solve_puzzle_one(self):
        return 'TODO'

    def solve_puzzle_two(self):
        return 'TODO'

    def print_results(self):
        start_time = self._get_current_time()
        ans_one, ans_two = self.solve_puzzles()
        elapsed_time = self._get_current_time() - start_time

        print('{} Day {:2d}-{}: {}'.format(self.year, self.day, 1, ans_one))
        print('{} Day {:2d}-{}: {}'.format(self.year, self.day, 2, ans_two))
        print('{}Elapsed Time: {} ms\n'.format(
            '*** ' if elapsed_time >= SLOW_ELAPSED_THRESHOLD else '',
            elapsed_time,
        ))

    def _get_current_time(self):
        return int(time() * 1000.0)

    def _get_input_directory(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        return '{}/../resources/dec{}/'.format(dir_path, self.year)

    def _get_input_filename(self):
        return '{}/{}-input'.format(self._get_input_directory(), self.day)

    def _load_all_input_lines(self, filename=None):
        if filename is None:
            filename = self._get_input_filename()
        elif '/' not in filename:
            filename = self._get_input_directory() + '/' + filename

        all_lines = []

        with open(filename) as f:
            for line in f:
                all_lines.append(line.strip('\n'))

        return all_lines
