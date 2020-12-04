import re

from aoc.common.day_solver import DaySolver


KEY_BIRTH_YEAR = 'byr'
KEY_ISSUE_YEAR = 'iyr'
KEY_EXPIRATION_YEAR = 'eyr'
KEY_HEIGHT = 'hgt'
KEY_HAIR_COLOR = 'hcl'
KEY_EYE_COLOR = 'ecl'
KEY_PASSPORT_ID = 'pid'
KEY_COUNTRY_ID = 'cid'

REQUIRED_KEYS = [
    KEY_BIRTH_YEAR,
    KEY_ISSUE_YEAR,
    KEY_EXPIRATION_YEAR,
    KEY_HEIGHT,
    KEY_HAIR_COLOR,
    KEY_EYE_COLOR,
    KEY_PASSPORT_ID,
]

REGEX_YEAR = re.compile(r'^(\d{4})$')
REGEX_HEIGHT = re.compile(r'^(\d+)(in|cm)$')
REGEX_HAIR_COLOR = re.compile(r'^(#)([0-9a-f]{6})$')
REGEX_PASSPORT_ID = re.compile(r'^(\d{9})$')

VALID_EYE_COLORS = ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']


class Day04Solver(DaySolver):
    year = 2020
    day = 4

    def solve_puzzle_one(self):
        passports = self._load_all_passports()

        valid_count = 0
        for p in passports:
            if self._does_passport_have_all_required_keys(p):
                valid_count += 1

        return valid_count

    def solve_puzzle_two(self):

        passports = self._load_all_passports()

        valid_count = 0
        for p in passports:
            if self._does_passport_have_all_required_keys(p) \
                    and self._is_passport_valid(p):
                valid_count += 1

        return valid_count

    def _load_all_passports(self):
        lines = self.load_all_input_lines()

        passports = []
        cur_line_num = 0
        current_passport = {}
        while cur_line_num < len(lines):
            cur_line = lines[cur_line_num]
            if not cur_line:
                if current_passport:
                    passports.append(current_passport)
                    current_passport = {}
            else:
                for data in cur_line.split(' '):
                    pair = data.split(':')
                    current_passport[pair[0]] = pair[1]

            cur_line_num += 1

        if current_passport:
            passports.append(current_passport)

        return passports

    def _does_passport_have_all_required_keys(self, passport):
        for key in REQUIRED_KEYS:
            if key not in passport:
                return False
        return True

    def _is_passport_valid(self, passport):
        if not self._is_valid_year_field(passport, KEY_BIRTH_YEAR, 1920, 2002):
            return False

        if not self._is_valid_year_field(passport, KEY_ISSUE_YEAR, 2010, 2020):
            return False

        if not self._is_valid_year_field(passport, KEY_EXPIRATION_YEAR, 2020, 2030):
            return False

        if not self._is_height_valid(passport):
            return False

        if not self._is_hair_color_valid(passport):
            return False

        if not self._is_hair_color_valid(passport):
            return False

        if not self._is_passport_id_valid(passport):
            return False

        return True

    def _match_regex_for_groups(self, passport, key, regex):
        value = passport.get(key)
        result = regex.match(value)
        if not result:
            return False
        return result.groups()

    def _is_valid_year_field(self, passport, key, min_year, max_year):
        groups = self._match_regex_for_groups(passport, key, REGEX_YEAR)
        if not groups:
            return False

        year = int(groups[0])
        return min_year <= year <= max_year

    def _is_height_valid(self, passport):
        groups = self._match_regex_for_groups(passport, KEY_HEIGHT, REGEX_HEIGHT)
        if not groups:
            return False

        hgt = int(groups[0])
        unit = groups[1]

        if unit == 'cm':
            return 150 <= hgt <= 193
        elif unit == 'in':
            return 59 <= hgt <= 76

        return True

    def _is_hair_color_valid(self, passport):
        groups = self._match_regex_for_groups(passport, KEY_HAIR_COLOR, REGEX_HAIR_COLOR)
        return bool(groups)

    def _is_eye_color_valid(self, passport):
        value = passport.get(KEY_EYE_COLOR)
        return value in VALID_EYE_COLORS

    def _is_passport_id_valid(self, passport):
        groups = self._match_regex_for_groups(passport, KEY_PASSPORT_ID, REGEX_PASSPORT_ID)
        return bool(groups)
