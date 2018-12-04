import re
from operator import attrgetter

from day_solver import DaySolver

INPUT_REGEX = re.compile('\[\d{4}-\d{2}-\d{2} \d{2}:(\d{2})] (.*)')

GUARD_REGEX = re.compile('Guard #(\d+) begins shift')
FALLS_ASLEEP = 'falls asleep'
WAKES_UP = 'wakes up'


class Day04Solver(DaySolver):
    year = 2018
    day = 4

    class GuardSleepProfile(object):
        def __init__(self, guard_id, guard_sleep_times):
            self.guard_id = guard_id
            self.total_sleep_time = 0

            self.most_common_minute = None
            self.max_minute_count = 0

            for time in range(0, 60):
                time_count = guard_sleep_times[time]

                self.total_sleep_time += time_count
                if time_count > self.max_minute_count:
                    self.max_minute_count = time_count
                    self.most_common_minute = time

        def calculate_answer(self):
            return self.guard_id * self.most_common_minute

    def solve_puzzles(self):
        guards = self._read_input()

        guard_sleep_profiles = map(lambda g: self.GuardSleepProfile(g, guards[g]), guards)

        sleepiest_guard = sorted(guard_sleep_profiles, key=attrgetter('total_sleep_time'), reverse=True)[0]
        consistent_guard = sorted(guard_sleep_profiles, key=attrgetter('max_minute_count'), reverse=True)[0]

        return sleepiest_guard.calculate_answer(), consistent_guard.calculate_answer()

    def _read_input(self):
        # Leading timestamps allow us to just sort the input and then process it
        entries = map(self._parse_line, sorted(self._load_all_input_lines()))

        guards = {}
        current_guard = None
        sleep_start_time = None

        for minute, entry in entries:
            if entry == FALLS_ASLEEP:
                sleep_start_time = minute
            elif entry == WAKES_UP:
                if sleep_start_time:
                    sleep_end_time = minute
                    self._record_sleep(guards, current_guard, sleep_start_time, sleep_end_time)
                    sleep_start_time = None
            else:
                shift_result = GUARD_REGEX.match(entry)
                if sleep_start_time is not None:
                    # If the previous guard didn't wake up before ending their shift, punch them through to 01:00
                    self._record_sleep(guards, current_guard, sleep_start_time, 60)
                    sleep_start_time = None
                current_guard = int(shift_result.group(1))

        return guards

    def _parse_line(self, line):
        result = INPUT_REGEX.match(line)
        minute = int(result.group(1))
        entry = result.group(2)

        return minute, entry

    def _record_sleep(self, guards, guard_id, sleep_start, sleep_end):
        # Use existing sleep counts by minute or create a new empty array
        current_sleep = guards[guard_id] if guard_id in guards else [0] * 60

        new_sleep = current_sleep[:sleep_start] \
            + [t+1 for t in current_sleep[sleep_start:sleep_end]] \
            + current_sleep[sleep_end:]

        guards[guard_id] = new_sleep
