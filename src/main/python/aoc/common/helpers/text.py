import re

ALL_DIGITS_REGEX = re.compile(r'\d+')
ALL_NUMBERS_REGEX = re.compile(r'-?\d+')


def parse_all_numbers(line):
    return [int(v) for v in ALL_NUMBERS_REGEX.findall(line)]


def decimal_to_binary(value, min_length=None):
    result = ''

    cur_value = value
    while cur_value > 0:
        result = str(cur_value % 2) + result
        cur_value //= 2

    if min_length:
        result = result.zfill(min_length)

    return result


def binary_to_decimal(value):
    return int(value, 2)


def hex_to_binary(value):
    out = str(bin(int(value, 16)))[2:]
    missing = len(out) % 8
    if missing:
        out = '0' * (8-missing) + out
    return out
