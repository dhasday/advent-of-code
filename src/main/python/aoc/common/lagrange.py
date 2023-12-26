import operator
from functools import reduce


def lagrange_polynomial_interpolation(target_x, x_values, y_values):
    """
    https://en.wikipedia.org/wiki/Lagrange_polynomial

    Interpolate the value for target_x based on known x and y values
    """
    def _basis(j):
        p = [(target_x - x_values[m]) / (x_values[j] - x_values[m]) for m in range(k) if m != j]
        return reduce(operator.mul, p)

    assert len(x_values) > 0 and len(x_values) == len(y_values)

    k = len(x_values)
    return sum(_basis(j) * y_values[j] for j in range(k))
