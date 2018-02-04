
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

# Total number of districts
NUM_DISTRICTS = 5

# Map dimension
GRID_DIM = 5

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

    # Keep track of each contiguous redistricting scheme
    contiguous_coords = []

    # Keep track of how many contiguous redistricting schemes are generated
    num_contiguous = 0

    for _ in range(NUM_REDISTRICTING_SCHEMES):
        # Get a random redistricting
        make_district_grid(district_grid, coords)

        if is_grid_contiguous(district_grid):
            num_contiguous += 1
            contiguous_coords.append(coords[:])

        shuffle(coords)

    message = "We generated " + str(num_contiguous) + " contiguous random redistricting schemes.\n"
    print_to_screen_and_file(message, text_file)

    # Keep track of how many times each party wins an election.
    num_wins = {
        G: 0,
        P: 0
    }

    # Keep track which ratio wins each election.
    # Key: 'num_green_wins:num_purple_wins'
    winning_ratios = {
      '2:3': 0,
      '3:2': 0,
      '4:1': 0,
      '5:0': 0
    }

    for contiguous_coord in contiguous_coords:
        grid = from_coords_to_grid(contiguous_coord)

        district_winners = get_district_winners(contiguous_coord)
        election_winner = get_election_winner(district_winners)
        winning_ratio = get_winning_ratio(district_winners)
        winning_ratios[winning_ratio] += 1
        num_wins[election_winner] += 1

    print_statistics(text_file, num_wins, winning_ratios, num_contiguous)

    print("\nStatistics report generated. See file '" + OUTPUT_FILE + "'.")

    text_file.close()

def get_percent_elections_won(num_wins, party, num_contiguous):
    """Get the percentage of elections won by a party

    :param num_wins: A dictionary containing parties as keys and election wins as values
    :return: The percent of total elections won
    """

    num_elections_won = num_wins[party]
    return num_elections_won / num_contiguous * 100

def print_statistics(text_file, num_wins, winning_ratios, num_contiguous):
    """Prints statistics of interest."""

    print_statistics_report_header(text_file)

    print_winning_ratios(text_file, winning_ratios, num_contiguous)

    for party in num_wins.keys():
        percent_won = get_percent_elections_won(num_wins, party, num_contiguous)
        print_percent_won(text_file, party, percent_won)

def print_statistics_report_header(text_file):
    """Print the header to the statistics report."""

    print_to_screen_and_file("STATISTICS REPORT", text_file)
    print_to_screen_and_file("-----------------", text_file)

def print_percent_won(text_file, party, percentage_won):
    """Print the percentage of elections the party won."""

    message = party + " won " + str(round(percentage_won, 2)) + "% percent of elections."
    print_to_screen_and_file(message, text_file)

def print_winning_ratios(text_file, winning_ratios, num_contiguous):
    for key in winning_ratios.keys():
        ratio = key.split(':')
        num_green_wins = ratio[0]
        num_purple_wins = ratio[1]
        message = "Green won " + num_green_wins + " districts "
        message += "and Purple won " + num_purple_wins + " districts "
        percent = winning_ratios[key] / num_contiguous * 100
        message += str(round(percent, 2)) + "% of the time."
        print_to_screen_and_file(message, text_file)
    print_to_screen_and_file("", text_file)  # Print extra newline character

def print_to_screen_and_file(message, file):
    """Prints a message to the screen and a file."""
    
    print(message)
    file.write(message + "\n")


def make_district_grid(district_grid, coords):
    """Mutate the redistricting scheme with a list of coordinates."""

    district = 1
    for i in range(1, len(coords) + 1):
        X = coords[i-1][0]
        Y = coords[i-1][1]
        district_grid[X][Y] = district
        if i % NUM_DISTRICTS == 0:
            district += 1

def from_coords_to_grid(coords):
    """Convert a list of coordinates into a grid."""

    grid = [[0] * GRID_DIM for _ in range(GRID_DIM)]
    district = 1
    for i in range(1, len(coords) + 1):
        X = coords[i-1][0]
        Y = coords[i-1][1]
        grid[X][Y] = district
        if i % NUM_DISTRICTS == 0:
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
    """A recursive helper function to find if a district is contiguous.

    Sources:
      * https://github.com/a1ip/checkio-1/blob/master/the%20Moore%20neighborhood.py
      * http://www.imageprocessingplace.com/downloads_V3/root_downloads/tutorials/contour_tracing_Abeer_George_Ghuneim/moore.html
    """

    if count == NUM_DISTRICTS:
        return True

    shifts = ((-1, -1), (-1,  0), (-1, 1), (0, -1),
              ( 0,  1), ( 1, -1), ( 1, 0), (1,  1))

    value = grid[curr_pos[0]][curr_pos[1]]

    for shift in shifts:
        shifted_X = curr_pos[0] + shift[0]
        shifted_Y = curr_pos[1] + shift[1]
        if is_in_bounds(grid, shifted_X, shifted_Y):
            neighbor = grid[shifted_X][shifted_Y]
            next_pos = (shifted_X, shifted_Y)
            if value == neighbor and next_pos not in prev_positions:
                prev_positions.add(next_pos)
                return is_district_contiguous_helper(grid, next_pos, prev_positions, count + 1)

def is_in_bounds(grid, x, y):
    """Get whether an (x, y) coordinate is within bounds of the grid."""

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

def get_district_winners(coords):
    """Get which party won each district from a list of coordinates.
    
    :param coords: A list of coordinates.
    :return: A dictionary where keys are districts,
             and values are parties.
    """

    districts = range(1, NUM_DISTRICTS + 1)
    district_winners = dict.fromkeys(districts)
    voter_map = get_voter_map()

    for i in range(NUM_DISTRICTS):
        district_coords = coords[5*i:5*(i+1)]
        num_green_votes = 0
        num_purple_votes = 0
        for coord in district_coords:
            if voter_map[coord[0]][coord[1]] == G:
                num_green_votes += 1
            else:
                num_purple_votes += 1
        if num_green_votes > num_purple_votes:
            district_winners[i+1] = G
        else:
            district_winners[i+1] = P

    return district_winners

def get_election_winner(district_winners):
    """Get which party won the election."""

    num_green_votes = 0
    num_purple_votes = 0
    for winner in district_winners.values():
        if winner == G:
            num_green_votes += 1
        else:
            num_purple_votes += 1
    if num_green_votes > num_purple_votes:
        return G
    else:
        return P

def get_winning_ratio(district_winners):
    """Get the ratio that won the election.

    The ratio that won the election,
    is the number of districts green won,
    versus the number of districts purple won.

    :return: A string with the number of districts green won,
             and the number of districts purple won,
             concatenated by a colon ':' character.
    """

    num_green_votes = 0
    num_purple_votes = 0
    for winner in district_winners.values():
        if winner == G:
            num_green_votes += 1
        else:
            num_purple_votes += 1
    return str(num_green_votes) + ':' + str(num_purple_votes)


if __name__ == '__main__':
    main()
