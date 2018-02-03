
'''
Name: G Roques
Date: 2/6/18
Course: [CS4500] Intro to the Software Profession - Section 001
Version: 1.0.0

Output Files:
  * HW3output.txt (generated in the same directory as the program)

Sources:
  * https://docs.python.org/
  * https://py.checkio.org/mission/count-neighbours/
  * https://github.com/a1ip/checkio-1/blob/master/the%20Moore%20neighborhood.py
  * http://www.imageprocessingplace.com/downloads_V3/root_downloads/tutorials/contour_tracing_Abeer_George_Ghuneim/moore.html

Description:
  A python program to explore redestricting schemes with a set of 25 voters.
  There are 15 green voters, and 10 purple voters. Making a 60-40 split.
  In each election, there is one green candidate, and one purple candidate in each district.
  Green voters always for the green candidate, and the purple voter always vote for the purple candidate.
  Statistics are output to the terminal and a file named "HW3output.txt".
'''

from random import shuffle
from itertools import product

# Name of output file
OUTPUT_FILE = "HW3output.txt"

# Total number of redistricting schemes
NUM_REDISTRICTING_SCHEMES = 1000  # 10 million

# Total number of voters
NUM_VOTERS = 25

# Total number of districts
NUM_DISTRICTS = 5

# Total number of voters in each district
NUM_VOTERS_IN_DISTRICT = 5

# Map dimension
GRID_DIM = 5

# Total number of green voters
MAX_GREEN_VOTERS = 15

# Total number of purple voters
MAX_PURPLE_VOTERS = 10

# Characters representing each party
P = 'Purple'
G = 'Green'

def main():
    text_file = open(OUTPUT_FILE, "w")

    # Initialize map of zeros
    district_grid = [[0] * GRID_DIM for _ in range(GRID_DIM)]

    # Start with a list of contiguous coordinates,
    # so that there's at least 1 contiguous redistricting scheme
    coords = get_contiguous_coords()

    contiguous_coords = []

    num_contiguous = 0

    for _ in range(NUM_REDISTRICTING_SCHEMES):
        # Get a random redistricting
        make_district_grid(district_grid, coords)

        if is_grid_contiguous(district_grid):
            num_contiguous += 1
            contiguous_coords.append(coords[:])

        shuffle(coords)

    print(str(num_contiguous) + " contiguous redistricting scheme\n")

    for contiguous_coord in contiguous_coords:
        grid = from_coords_to_grid(contiguous_coord)
        for row in grid:
            print(row)
        print("")

    text_file.close()

def make_district_grid(district_grid, coords):
    """Mutate the redistricting scheme with a list of coordinates."""

    district = 1
    for i in range(1, len(coords) + 1):
        X = coords[i-1][0]
        Y = coords[i-1][1]
        district_grid[X][Y] = district
        if i % 5 == 0:
            district += 1

def from_coords_to_grid(coords):
    """Convert a list of coordinates into a grid."""

    grid = [[0] * GRID_DIM for _ in range(GRID_DIM)]
    district = 1
    for i in range(1, len(coords) + 1):
        X = coords[i-1][0]
        Y = coords[i-1][1]
        grid[X][Y] = district
        if i % 5 == 0:
            district += 1
    return grid

def get_voter_map():
    """Get a 5x5 map representing the location of the voters.

    P - Purple
    G - Green
    """

    return [[P, G, G, G, G],
            [G, P, P, P, G],
            [G, P, G, G, G],
            [G, G, G, P, P],
            [P, G, P, G, P]]

def get_contiguous_coords():
    """Get a list of coordinates to construct a contiguous redistricting scheme."""

    return [(0, 0), (1, 1), (1, 2), (2, 2), (3, 2),
            (0, 1), (1, 0), (2, 0), (2, 1), (3, 1),
            (3, 0), (4, 0), (4, 1), (4, 2), (3, 3),
            (0, 2), (0, 3), (0, 4), (1, 4), (2, 4),
            (1, 3), (2, 3), (3, 4), (4, 4), (4, 3)]

def is_grid_contiguous(grid):
    """Check whether the grid is contiguous."""

    start_positions = find_start_positions(grid)
    for start_pos in start_positions.values():
        if not is_district_contiguous(grid, start_pos):
            return False
    return True


def is_district_contiguous(grid, start_pos):
    """Check whether the district is contiguous."""

    prev_positions = set()
    prev_positions.add(start_pos)
    return is_district_contiguous_helper(grid, start_pos, prev_positions, 1)

def is_district_contiguous_helper(grid, curr_pos, prev_positions, count):
    """Find whether the district is contiguous.

    Source: https://github.com/a1ip/checkio-1/blob/master/the%20Moore%20neighborhood.py
    Source: http://www.imageprocessingplace.com/downloads_V3/root_downloads/tutorials/contour_tracing_Abeer_George_Ghuneim/moore.html
    """

    if count == 5:
        return True
    shifts = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    value = grid[curr_pos[0]][curr_pos[1]]
    found_neighbor = 0
    for shift in shifts:
        n_row = curr_pos[0] + shift[0]
        n_col = curr_pos[1] + shift[1]
        if is_in_bounds(grid, n_row, n_col):
            new_value = grid[n_row][n_col]
            new_curr_pos = (n_row, n_col)
            if value == new_value and new_curr_pos not in prev_positions:
                prev_positions.add(new_curr_pos)
                return is_district_contiguous_helper(grid, new_curr_pos, prev_positions, count + 1)
    if found_neighbor == 0:
        return False

def is_in_bounds(grid, x, y):
    return (x >= 0 and x < len(grid)) and (y >= 0 and y < len(grid[0]))

def find_start_positions(grid):
    """Find the first position of each district within the grid.

    :return: A dictionary where the keys are districts,
             and the values are tuples representing an (x, y) coordinate.
    """

    districts = range(1, NUM_DISTRICTS + 1)
    start_positions = dict.fromkeys(districts)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            district = grid[i][j]
            if start_positions[district] is None:
                start_positions[district] = (i, j)
            if None not in start_positions.values():
                break
    return start_positions

if __name__ == '__main__':
    main()
