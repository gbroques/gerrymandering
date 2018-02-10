"""
Helper functions for operating on a set of coordinates.
"""

from constants import G
from constants import NUM_DISTRICTS
from constants import P
from util import get_voter_map


def get_districts_from_coordinates(coordinates):
    """Returns a list of districts from a list coordinates.

    The districts are in order of appearance in the grid.
    Therefore, (0, 0) is the first element,
    and (4, 4) is the last element of the list.

    :param coordinates: A list of coordinates.
    :return: A list of districts in order of appearance in the grid.
    """
    districts = [0 for _ in range(len(coordinates))]
    district = 1
    for i in range(1, len(coordinates) + 1):
        x = coordinates[i - 1][0]
        y = coordinates[i - 1][1]
        index = (x * NUM_DISTRICTS) + y
        districts[index] = district
        if i % NUM_DISTRICTS == 0:
            district += 1
    return districts


def get_district_winners(coordinates):
    """Get which party won each district from a list of coordinates.

    :param coordinates: A list of coordinates.
    :return: A dictionary where keys are districts,
             and values are parties.
    """

    districts = range(1, NUM_DISTRICTS + 1)
    district_winners = dict.fromkeys(districts)
    voter_map = get_voter_map()

    for i in range(NUM_DISTRICTS):
        district_coordinates = coordinates[NUM_DISTRICTS * i:NUM_DISTRICTS * (i + 1)]
        num_green_votes = 0
        num_purple_votes = 0
        for coord in district_coordinates:
            if voter_map[coord[0]][coord[1]] == G:
                num_green_votes += 1
            else:
                num_purple_votes += 1
        if num_green_votes > num_purple_votes:
            district_winners[i + 1] = G
        else:
            district_winners[i + 1] = P

    return district_winners


def from_coordinates_to_grid(coordinates):
    """Convert a list of coordinates into a grid."""

    grid = [[0] * NUM_DISTRICTS for _ in range(NUM_DISTRICTS)]
    district = 1
    for i in range(1, len(coordinates) + 1):
        x = coordinates[i - 1][0]
        y = coordinates[i - 1][1]
        grid[x][y] = district
        if i % NUM_DISTRICTS == 0:
            district += 1
    return grid

