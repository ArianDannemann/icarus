"""
Module to help with some operations on positions
"""


def equals(a, b):
    """
    Returns true if a[0]==b[0] and a[1]==b[1]
    """

    return (a[0] == b[0] and a[1] == b[1])


def is_in_bounds(a):
    """
    Returns true if a[0] and a[1] are within the bounds of 0 to 7
    """

    return not (a[0] > 7 or a[0] < 0 or a[1] > 7 or a[1] < 0)
