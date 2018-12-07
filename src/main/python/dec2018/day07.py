import re

from common.day_solver import DaySolver

INPUT_REGEX = re.compile('Step ([A-Z]) must be finished before step ([A-Z]) can begin.')


class Day07Solver(DaySolver):
    year = 2018
    day = 7

    class Worker(object):
        cur_step = None
        time_remaining = 0

        def is_available(self):
            return self.time_remaining <= 0

        def start_step(self, step):
            self.cur_step = step
            self.time_remaining = 61 + ord(step) - ord('A')

        def tick_time(self, ticks):
            if self.time_remaining is not None:
                self.time_remaining -= ticks

        def complete_step(self):
            step = self.cur_step
            self.cur_step = None
            return step

        def __str__(self):
            return '{} - {} secs'.format(self.cur_step, self.time_remaining)

    def solve_puzzle_one(self):
        requirements = self._load_input()

        result = ''
        completed_steps = []

        while len(result) < len(requirements):
            available = self._get_available_steps(requirements, completed_steps)

            result += available[0]
            completed_steps.append(available[0])

        return result

    def solve_puzzle_two(self):
        requirements = self._load_input()

        result = ''
        completed_steps = []
        assigned = []
        workers = list([self.Worker() for _ in range(5)])

        total_ticks = 0
        while len(result) < len(requirements):
            ticks = self._advance_to_next_completed_step(workers)
            if ticks:
                total_ticks += ticks

            completed = self._get_completed_steps(workers)
            for s in sorted(completed):
                result += s
                completed_steps.append(s)

            available_steps = self._get_available_steps(requirements, completed_steps, assigned)
            assigned.extend(self._assign_available_steps(workers, available_steps))

        return total_ticks

    def _load_input(self):
        requirements = dict()

        for l in self._load_all_input_lines():
            step, req = self._load_line(l)

            if req not in requirements:
                requirements[req] = []

            if step not in requirements:
                requirements[step] = []

            requirements[step].append(req)

        return requirements

    def _load_line(self, line):
        result = INPUT_REGEX.match(line)

        step = result.group(2)
        req = result.group(1)

        return step, req

    def _get_available_steps(self, requirements, completed_steps, assigned=[]):
        available = []
        for step in requirements:
            reqs = requirements[step]

            if step in completed_steps or step in assigned:
                continue

            if self._are_all_reqs_completed(completed_steps, reqs):
                available.append(step)

        return sorted(available)

    def _are_all_reqs_completed(self, completed_steps, reqs):
        for r in reqs:
            if r not in completed_steps:
                return False
        return True

    def _advance_to_next_completed_step(self, workers):
        min_remaining = None
        for w in workers:
            if not w.is_available():
                if min_remaining is None or w.time_remaining < min_remaining:
                    min_remaining = w.time_remaining

        if min_remaining:
            for w in workers:
                w.tick_time(min_remaining)

        return min_remaining

    def _get_completed_steps(self, workers):
        completed = []

        for w in workers:
            if w.is_available() and w.cur_step is not None:
                completed.append(w.complete_step())

        return completed

    def _assign_available_steps(self, workers, available_steps):
        assigned = []

        for w in workers:
            if w.is_available() and len(available_steps) > 0:
                new_step = available_steps.pop(0)
                w.start_step(new_step)
                assigned.append(new_step)

        return assigned
