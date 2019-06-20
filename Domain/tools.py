import math
from typing import List


def covariance(x: List, y: List) -> float:
    """
    :param x: Variable X
    :param y: Variable Y
    :return: Covariance between X and Y
    """
    if len(x) != len(y):
        raise RuntimeError(f"The number of entries of x and Y should be the same to calculate the covariance: "
                           f"X:{len(x)}, Y:{len(y)}")
    expected_x = sum(x) / len(x)
    expected_y = sum(y) / len(y)
    cov = 0
    for i in range(len(x)):
        cov += (x[i] - expected_x) * (y[i] - expected_y)
    cov = cov / len(x)
    return cov


def variance(x: List) -> float:
    """
    :param x: Variable X
    :return: Variance of X
    """
    expected_x = sum(x) / len(x)
    var = 0
    for i in range(len(x)):
        var += (x[i] - expected_x) * (x[i] - expected_x)
    var /= len(x)
    return var


def standard_deviation(x: List) -> float:
    """
    :param x: Variable X
    :return: Standard Deviation of Variable X
    """
    return math.sqrt(variance(x))


