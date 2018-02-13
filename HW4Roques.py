"""
Name: G Roques
Date: 2/6/18
Course: [CS4500] Intro to the Software Profession - Section 001
Version: 1.0.0

Output Files:
  * HW4output.txt (generated in the same directory as the program)

Sources:
  * https://docs.python.org/
  * https://py.checkio.org/mission/count-neighbours/
  * https://github.com/a1ip/checkio-1/blob/master/the%20Moore%20neighborhood.py
  * http://www.imageprocessingplace.com/downloads_V3/root_downloads/tutorials/contour_tracing_Abeer_George_Ghuneim/moore.html
  * https://stackoverflow.com/questions/26988204/using-2d-array-to-create-clickable-tkinter-canvas

Description:
  A python program to explore redistricting schemes with a set of 25 voters.
  There are 15 green voters, and 10 purple voters. Making a 60-40 split.
  In each election, there is one green candidate, and one purple candidate in each district.
  Green voters always for the green candidate, and the purple voter always vote for the purple candidate.
  Statistics are output to the terminal and a file named "HW4output.txt".

  To get 30 contiguous random redistrictings it might take around 1 billion iterations,
  and 16 hours depending upon your machine.
"""

import sys
from random import shuffle

from constants import NUM_DISTRICTS
from constants import NUM_ITERATIONS_TO_PRINT_DOT
from constants import NUM_REDISTRICTING_SCHEMES
from contiguous_data import get_contiguous_coordinates
from contiguous_data import get_second_contiguous_coordinates
from gui import App
from output_printer import OutputPrinter


def main():
    # Initialize grid of zeros
    district_grid = initialize_district_grid(0)

    # Start with a list of contiguous coordinates,
    # so that there's at least 1 contiguous redistricting scheme
    coordinates = get_contiguous_coordinates()

    # Keep track of each contiguous redistricting scheme
    contiguous_coordinate_list = []

    # Add another set of contiguous coordinates to list,
    # so that you don't have to wait so long to see results.
    contiguous_coordinate_list.append(get_second_contiguous_coordinates())

    for i in range(NUM_REDISTRICTING_SCHEMES):
        redistrict_grid(district_grid, coordinates)

        if is_grid_contiguous(district_grid):
            contiguous_coordinate_list.append(coordinates[:])

        shuffle(coordinates)

        print_loading_dots(i)

    # TODO: Give output printer a more descriptive name
    output_printer = OutputPrinter(contiguous_coordinate_list)
    output_printer.print_output()

    # Run GUI application
    gui = App(contiguous_coordinate_list, output_printer.winning_ratios)
    gui.run_mainloop()


def initialize_district_grid(initial_value):
    return [[initial_value] * NUM_DISTRICTS for _ in range(NUM_DISTRICTS)]


def redistrict_grid(district_grid, coordinates):
    """Redistrict grid with a list of coordinates."""
    district = 1
    for i in range(1, len(coordinates) + 1):
        x = coordinates[i - 1][0]
        y = coordinates[i - 1][1]
        district_grid[x][y] = district
        if i % NUM_DISTRICTS == 0:
            district += 1


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
    """A recursive helper function to find if a district is contiguous.

    Sources:
      * https://github.com/a1ip/checkio-1/blob/master/the%20Moore%20neighborhood.py
      * http://www.imageprocessingplace.com/downloads_V3/root_downloads/tutorials/contour_tracing_Abeer_George_Ghuneim/moore.html
    """
    if count == NUM_DISTRICTS:
        return True

    shifts = ((-1, -1), (-1, 0), (-1, 1), (0, -1),
              (0, 1), (1, -1), (1, 0), (1, 1))

    value = grid[curr_pos[0]][curr_pos[1]]

    for shift in shifts:
        shifted_x = curr_pos[0] + shift[0]
        shifted_y = curr_pos[1] + shift[1]
        if is_in_bounds(grid, shifted_x, shifted_y):
            neighbor = grid[shifted_x][shifted_y]
            next_pos = (shifted_x, shifted_y)
            if value == neighbor and next_pos not in prev_positions:
                prev_positions.add(next_pos)
                return is_district_contiguous_helper(grid, next_pos, prev_positions, count + 1)


def is_in_bounds(grid, x, y):
    """Get whether an (x, y) coordinate is within bounds of the grid."""
    return (0 <= x < len(grid)) and (0 <= y < len(grid[0]))


def find_start_positions(grid):
    """Find the first position of each district within the grid.

    TODO: Refactor to get start positions from the list of coordinates,
          rather than grid to improve performance.

    :param grid: Grid of districts.
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


def print_loading_dots(i):
    """Print dots to indicate loading to the user.

    :param i: Number of iterations.
    :return: void
    """
    if i % NUM_ITERATIONS_TO_PRINT_DOT == 0:
        print('.', end='')
        sys.stdout.flush()
    elif i == NUM_REDISTRICTING_SCHEMES - 1:
        print('\n')


if __name__ == '__main__':
    main()
