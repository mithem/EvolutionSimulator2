import math


def base(self, x_not_needed=0, base=0):
    return base


def linear(self, x, base):
    return x * base * 0.01


def sqrt(self, x, base_not_needed=0):
    return math.sqrt(x) * 100


def fraction(self, x, base_not_needed=0):
    return (1 / (x + 1)) * 10000


def negative_parabola(self, x, base):
    return -0.0008 * (x**2) + base


def fourth_grade(self, x, base):
    return (x**4 - (x**2 * 10000)) / 100000
