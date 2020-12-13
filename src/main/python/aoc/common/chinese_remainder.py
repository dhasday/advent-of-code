from functools import reduce


# Chinese Remainder code from
# https://rosettacode.org/wiki/Chinese_remainder_theorem#Python_3.6
def chinese_remainder(divisors, remainders):
    total = 0
    prod = reduce(lambda a, b: a * b, divisors)
    for n_i, a_i in zip(divisors, remainders):
        p = prod // n_i
        total += a_i * mul_inv(p, n_i) * p
    return total % prod


def mul_inv(a, b):
    b0 = b
    x0, x1 = 0, 1
    if b == 1:
        return 1

    while a > 1:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += b0
    return x1
