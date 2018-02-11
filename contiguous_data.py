"""
Contains methods for getting contiguous redistricting schemes as sets of coordinates.
"""

from itertools import product
from constants import NUM_DISTRICTS


def get_contiguous_coordinates():
    """Get a list of coordinates to construct a contiguous redistricting scheme.

    First five elements comprise district 1,
    next five elements comprise district 2,
    and so on.
    """
    return [(0, 0), (1, 1), (1, 2), (2, 2), (3, 2),
            (0, 1), (1, 0), (2, 0), (2, 1), (3, 1),
            (3, 0), (4, 0), (4, 1), (4, 2), (3, 3),
            (0, 2), (0, 3), (0, 4), (1, 4), (2, 4),
            (1, 3), (2, 3), (3, 4), (4, 4), (4, 3)]


def get_second_contiguous_coordinates():
    """Get a list of coordinates to construct a contiguous redistricting scheme.

    First five elements comprise district 1,
    next five elements comprise district 2,
    and so on.
    """
    return list(product(range(NUM_DISTRICTS), repeat=2))
