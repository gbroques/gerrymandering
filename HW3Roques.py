
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
NUM_REDISTRICTING_SCHEMES = 1000  # 1 million

# Total number of voters
NUM_VOTERS = 25

# Total number of districts
NUM_DISTRICTS = 5

# Total number of voters in each district
NUM_VOTERS_IN_DISTRICT = 5

# Map dimension
MAP_DIM = 5

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
    district_map = [[0] * MAP_DIM for _ in range(MAP_DIM)]

    # Get a random list of coordinates
    coords = list(product(range(MAP_DIM), repeat=2))
    shuffle(coords)

    # Get random redistricting
    district = 1
    for i in range(1, len(coords) + 1):
        X = coords[i-1][0]
        Y = coords[i-1][1]
        district_map[X][Y] = district
        if i % 5 == 0:
            district += 1

    contiguous_grid = get_contiguous_grid()
    print("CONTIGUOUS GRID")
    for row in contiguous_grid:
        print(row)

    if is_grid_contiguous(contiguous_grid):
        print("Grid is contiguous\n\n")
    else:
        print("Grid is not contiguous\n\n")

    non_contiguous_grid = get_non_contiguous_grid()
    print("NON CONTIGUOUS GRID")
    for row in non_contiguous_grid:
        print(row)

    if is_grid_contiguous(non_contiguous_grid):
        print("Grid is contiguous")
    else:
        print("Grid is not contiguous")


    text_file.close()

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

def get_contiguous_grid():
    """Get a contiguous grid representing a redistricting scheme."""

    return [[1, 2, 4, 4, 4],
            [2, 1, 1, 5, 4],
            [2, 2, 1, 5, 4],
            [3, 2, 1, 3, 5],
            [3, 3, 3, 5, 5]]

def get_non_contiguous_grid():
    """Get a non-contiguous redistricting scheme."""

    return [[1, 2, 4, 4, 4],
            [2, 1, 1, 5, 4],
            [2, 2, 1, 5, 4],
            [3, 2, 3, 3, 5],
            [3, 3, 3, 5, 5]]

def is_grid_contiguous(grid):
    start_positions = find_start_positions(grid)
    for start_pos in start_positions.values():
        if not is_district_contiguous(grid, start_pos):
            return False
    return True


def is_district_contiguous(grid, start_pos):
    prev_positions = set()
    prev_positions.add(start_pos)
    return is_district_contiguous_helper(grid, start_pos, prev_positions, 1)

def is_district_contiguous_helper(grid, curr_pos, prev_positions, count):
    """Find whetere the district is contiguous.

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
        if (n_row >= 0 and n_row < len(grid)) and (n_col >= 0 and n_col < len(grid[0])):  ## Bounds checking
            new_value = grid[n_row][n_col]
            new_curr_pos = (n_row, n_col)
            if value == new_value and new_curr_pos not in prev_positions:
                prev_positions.add(new_curr_pos)
                return is_district_contiguous_helper(grid, new_curr_pos, prev_positions, count + 1)
    if found_neighbor == 0:
        return False

def find_start_positions(grid):
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
