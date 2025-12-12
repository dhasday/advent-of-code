import math


def lcm(values):
    _lcm = values[0]
    for v in values[1:]:
        gcd = math.gcd(_lcm, v)
        _lcm = abs(_lcm * v) // gcd

    return _lcm
