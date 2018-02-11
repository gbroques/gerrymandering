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

from constants import G
from constants import NUM_DISTRICTS
from constants import NUM_REDISTRICTING_SCHEMES
from constants import P
from contiguous_data import get_contiguous_coordinates
from contiguous_data import get_second_contiguous_coordinates
from coordinates import from_coordinates_to_grid
from coordinates import get_district_winners
from district_winners import get_election_winner
from district_winners import get_winning_ratio
from gui import App
from statistics import print_statistics
from util import get_border
from util import get_voter_map
from util import print_to_screen_and_file

# Name of output file
OUTPUT_FILE = "HW4output.txt"


def main():
    text_file = open(OUTPUT_FILE, "w")

    # Initialize map of zeros
    district_grid = [[0] * NUM_DISTRICTS for _ in range(NUM_DISTRICTS)]

    # Start with a list of contiguous coordinates,
    # so that there's at least 1 contiguous redistricting scheme
    coordinates = get_contiguous_coordinates()

    # Keep track of each contiguous redistricting scheme
    contiguous_coordinates = []

    # Keep track of how many contiguous redistricting schemes are generated
    num_contiguous = 0

    contiguous_coordinates.append(get_second_contiguous_coordinates())
    num_contiguous += 1

    for i in range(NUM_REDISTRICTING_SCHEMES):
        # Get a random redistricting
        make_district_grid(district_grid, coordinates)

        if is_grid_contiguous(district_grid):
            num_contiguous += 1
            contiguous_coordinates.append(coordinates[:])

        shuffle(coordinates)

        print_loading_dots(i)

    print('\n')

    message = 'We generated ' + str(num_contiguous) + ' contiguous random redistricting schemes.\n'
    print_to_screen_and_file(message, text_file)

    # Keep track of how many times each party wins an election.
    num_wins = {
        G: 0,
        P: 0
    }

    winning_ratios = get_winning_ratios()

    for contiguous_coordinate in contiguous_coordinates:
        grid = from_coordinates_to_grid(contiguous_coordinate)
        print_district_map(text_file, grid)

        district_winners = get_district_winners(contiguous_coordinate)
        election_winner = get_election_winner(district_winners)
        winning_ratio = get_winning_ratio(district_winners)
        winning_ratios[winning_ratio] += 1
        num_wins[election_winner] += 1

    print_legend(text_file)

    print_statistics(text_file, num_wins, winning_ratios, num_contiguous)

    print_output_file_generated_message()

    text_file.close()

    # Run GUI application
    gui = App(contiguous_coordinates, winning_ratios)
    gui.run_mainloop()


def get_winning_ratios():
    """Get a dictionary to keep track which ratio wins each election.

    Key: 'num_green_wins:num_purple_wins'
    :return: Winning ratios dictionary.
    """
    return {
        '2:3': 0,
        '3:2': 0,
        '4:1': 0,
        '5:0': 0
    }


def print_loading_dots(i):
    """Print dots to indicate loading to the user.

    Prints one dot every 2 million iterations.
    Prints 50 dots for 100 million iterations.

    :param i: Number of iterations.
    :return: void
    """
    if i % 2000000 == 0:
        print('.', end='')
        sys.stdout.flush()


def make_district_grid(district_grid, coordinates):
    """Mutate the redistricting scheme with a list of coordinates."""
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


def print_district_map(text_file, district_map):
    voter_map = get_voter_map()
    border_length = 20
    border = get_border('═', border_length)
    print_to_screen_and_file('╔' + border + '╗', text_file)
    for i in range(len(district_map)):
        print_to_screen_and_file('║', text_file, end='')
        for j in range(len(district_map[i])):
            party = voter_map[i][j]
            display_str = str(district_map[i][j]) + party[0]
            print_to_screen_and_file(' ' + display_str + ' ', text_file, end='')
        print_to_screen_and_file('║', text_file)
    print_to_screen_and_file('╚' + border + '╝\n', text_file)


def print_legend(text_file):
    print_to_screen_and_file('LEGEND', text_file)
    print_to_screen_and_file('  G - Green', text_file)
    print_to_screen_and_file('  P - Purple\n', text_file)


def print_output_file_generated_message():
    print("\nStatistics report generated. See file '" + OUTPUT_FILE + "'.")


if __name__ == '__main__':
    main()
