from abc import ABCMeta, abstractmethod, abstractproperty
from time import time
import os

SLOW_ELAPSED_THRESHOLD_MS = 5000

RESULT_FORMAT = '{} Day {:2d}-{}: {}'


class DaySolver(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        super(DaySolver, self).__init__()

    def solve_puzzles(self):
        self.setup()
        return self.solve_puzzle_one(), self.solve_puzzle_two()

    @property
    @abstractmethod
    def year(self):
        pass

    @property
    @abstractmethod
    def day(self):
        pass

    def setup(self):
        pass

    def solve_puzzle_one(self):
        return 'TODO'

    def solve_puzzle_two(self):
        return 'TODO'

    def print_results(self, enable_timer=True):
        if enable_timer:
            start_time = self._get_current_time()
            ans_one, ans_two = self.solve_puzzles()
            elapsed_time = self._get_current_time() - start_time

            self._print_answer_part(1, ans_one)
            self._print_answer_part(2, ans_two)
            print('{}Elapsed Time: {} ms\n'.format(
                '*** ' if elapsed_time >= SLOW_ELAPSED_THRESHOLD_MS else '',
                elapsed_time,
            ))
        else:
            ans_one, ans_two = self.solve_puzzles()
            self._print_answer_part(1, ans_one)
            self._print_answer_part(2, ans_two)

    def _print_answer_part(self, part_num, ans):
        print(RESULT_FORMAT.format(self.year, self.day, part_num, ans))

    def _get_current_time(self):
        return int(time() * 1000.0)

    def _get_input_directory(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        return '{}/../../../resources/dec{}/'.format(dir_path, self.year)

    def _get_input_filename(self, filename=None):
        if filename is None:
            return '{}/{}-input'.format(self._get_input_directory(), self.day)
        else:
            return '{}/{}'.format(self._get_input_directory(), filename)

    def load_only_input_line(self, filename=None):
        filename = self._get_input_filename(filename)

        with open(filename) as f:
            return f.readline()

    def load_all_input_lines(self, filename=None):
        filename = self._get_input_filename(filename)

        with open(filename) as f:
            return [line.strip('\n') for line in f]
