from abc import ABCMeta, abstractmethod, abstractproperty
from time import time

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

    @abstractmethod
    def solve_puzzle_one(self):
        pass

    @abstractmethod
    def solve_puzzle_two(self):
        pass

    def print_results(self):
        start_time = self._get_current_time()
        ans_one, ans_two = self.solve_puzzles()
        elapsed_time = self._get_current_time() - start_time

        print('{} Day {:2d}-{}: {}'.format(self.year, self.day, 1, ans_one))
        print('{} Day {:2d}-{}: {}'.format(self.year, self.day, 2, ans_two))
        print('{}Elapsed Time: {} ms'.format(
            '*** ' if elapsed_time >= SLOW_ELAPSED_THRESHOLD else '',
            elapsed_time,
        ))

    def _get_current_time(self):
        return int(time() * 1000.0)
