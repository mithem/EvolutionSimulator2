import math


def base(x=0, base=0):
    return base


def linear(x=0, base=0):
    return x * base


def sqrt(x, base=0):
    return math.sqrt(x) * 100


def fraction(x, base=0):
    return (1 / (x + 1)) * 10000


def negative_parabola(x, base):
    return -0.0008 * (x**2) + base


def fourth_grade(x, base):
    return (x**4 - (x**2 * 10000)) / 100000
