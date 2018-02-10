"""
Functions for dealing with district winners.
"""

from constants import G
from constants import P


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

